import yaml
from .request import Request
import uuid
import logging
import jsonschema

logger = logging.getLogger(__name__)


class Node:
    """Class for store node"""

    def __init__(self, obj: Request, prev, next):
        self.obj = obj
        self.prev = prev
        self.next = next


class GlobalVariable(dict):
    """Class for store global variables"""

    DEFAULT_FILENAME = "global_vars.yaml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enabled = True
        self.filename = self.DEFAULT_FILENAME

    def load_config(self, config: dict):
        if config is None or not isinstance(config, dict):
            raise ValueError("Config must be dict")

        self.enabled = config.get("enabled", True)
        self.filename = config.get("filename", self.DEFAULT_FILENAME)

    def save(self):
        """Save global variables to file"""
        # Exclude object in global variable
        if not self.enabled:
            return

        string_variable = {}
        for key, value in self.items():
            if isinstance(value, str):
                string_variable[key] = value

        with open(self.filename, "w") as f:
            yaml.dump(string_variable, f)


class RequestChain:
    """Class for RequestChain store linked list"""

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None

        self.node_list = []
        self.node_dict = {}
        self.global_vars = GlobalVariable({"uuid4": lambda: str(uuid.uuid4())})
        self.proxy_config = None
        self.support_chains = {}
        self.request_responses = []

    def add(self, obj, name):
        """Add object to linked list"""
        if self.head is None:
            self.head = Node(obj, None, None)
            self.tail = self.head
            self.node_list.append(self.head)
            self.node_dict[name] = self.head
        else:
            self.tail.next = Node(obj, self.tail, None)
            self.tail = self.tail.next
            self.node_list.append(self.tail)
            self.node_dict[name] = self.tail

    def run(
        self, custom_vars: dict | None = None, custom_support_chains: dict | None = None
    ):
        """Run all requests"""
        if custom_vars is not None and isinstance(custom_vars, dict):
            self.global_vars.update(custom_vars)

        if custom_support_chains is not None and isinstance(
            custom_support_chains, dict
        ):
            self.support_chains.update(custom_support_chains)

        curr = self.head
        while curr is not None:
            request_response = curr.obj.run(
                self.global_vars, self.proxy_config, self.support_chains
            )
            self.request_responses.append(request_response)
            curr = curr.next

            if self.global_vars.get("skip_the_chain", False):
                break

            if self.global_vars.get("delay_time", 0) > 0:
                import time

                logger.warning(f"Delay {self.global_vars.get('delay_time')} seconds")
                time.sleep(self.global_vars.get("delay_time"))

        self.global_vars.save()

        return self.request_responses

    @staticmethod
    def parse_config(filename: str) -> object:
        """Parse yaml config file"""

        from pathlib import Path

        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError(f"File {filename} not found")

        # Path đến file hiện tại
        current_file = Path(__file__).resolve()
        # Thư mục chứa file
        current_dir = current_file.parent

        with open(current_dir / "schema.yaml", "r") as f:
            schema = yaml.safe_load(f)

        with path.open(mode="r") as f:
            data = yaml.safe_load(f)

        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            print(f"Validation ERROR in '{path.name}':")
            print(e)
            exit(-1)
        except yaml.YAMLError as e:
            print(f"Lỗi khi đọc file YAML (cấu hình hoặc schema): {e}")
            exit(-1)
        except Exception as e:
            print(f"Đã xảy ra lỗi không mong muốn: {e}")
            exit(-1)

        chain = data.get("chain")
        if not isinstance(chain, list):
            raise ValueError("Chain not found in config file")

        proxy_config = data.get("proxy", None)
        global_vars = data.get("global_vars", {})

        if not isinstance(global_vars, dict):
            raise ValueError("Global vars must be dict")

        if proxy_config is not None:
            if not isinstance(proxy_config, dict):
                raise ValueError("Proxy config must be dict")
            try:
                proxy_config.get("host")
                proxy_config.get("port")
            except AttributeError:
                raise ValueError("Proxy config must have host and port")

        base_dir = path.parent

        req_chain: RequestChain = RequestChain()
        # Load global vars
        req_chain.global_vars.update(global_vars)
        req_chain.global_vars.load_config(data.get("__persistence__", {}))

        # Load Stored variable
        try:
            with open(req_chain.global_vars.DEFAULT_FILENAME, "r") as f:
                stored_vars = yaml.safe_load(f)
                req_chain.global_vars.update(stored_vars)
        except FileNotFoundError:
            pass

        req_chain.proxy_config = proxy_config

        for req in chain:
            req_conf = req.get("req")
            if not isinstance(req_conf, dict):
                raise ValueError("Request not found in config file")

            req_obj = Request.parse_request(base_dir, req_conf)

            req_chain.add(req_obj, req_conf.get("name"))

        # Support chain like login
        support_chains = [i for i in data.keys() if i.endswith("_chain")]
        for support_chain in support_chains:
            support_chain_reqs = RequestChain()
            support_chain_reqs.proxy_config = proxy_config
            support_chain_reqs.global_vars = req_chain.global_vars

            req_chain.support_chains[support_chain] = None
            chain = data[support_chain]
            for req in chain:
                req_conf = req.get("req")
                if not isinstance(req_conf, dict):
                    raise ValueError("Request not found in config file")
                req_obj = Request.parse_request(base_dir, req_conf)
                support_chain_reqs.add(req_obj, req_conf.get("name"))

            req_chain.support_chains[support_chain] = support_chain_reqs

        return req_chain
