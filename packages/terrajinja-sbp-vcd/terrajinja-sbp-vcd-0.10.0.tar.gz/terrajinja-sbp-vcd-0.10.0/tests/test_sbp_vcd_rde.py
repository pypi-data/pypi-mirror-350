import json
import pytest
from cdktf import Testing
from src.terrajinja.sbp.vcd.rde import SbpVcdRde
from .helper import stack, has_resource, has_resource_count


class TestSbpVcdNsxtAlbVirtualService:

    def test_resource(self, stack):
        pool = SbpVcdRde(
            scope=stack,
            ns="rde",
            name="mycluster002",
            vcd_org="OFD",
            vcd_org_vdc="OFD-TST",
            loadbalancer_subnet="10.213.254.1/24",
            network_name="OFD-TST-SHR-K8S",
            kubernetes_api_ip="10.213.4.101",
            ssh_public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCiLzCIZMjNbQmjoD+xAChEDKpZmz/23R8qQi0L4c2zFk3DUzc5l0Xx/tJFgd45oifd4ES1gnN8k3eAsZ2GvrjO4Fai5yxkwpyBoIeYlp0cH+WyKQSxMwmmycuSXBK4nWNLegkpjziEqFySJRABdmcq9apqcf1rEAn1xk6X7fr7ox5p8We+thVCMVneMU4KouBegwVL48HXcKvsOWQ18NCqr3Z5DM58U9Ku3QbDqD9V7Un4C27EnivJT1yOZL0CflVC1nh+crQ88AxfENsyfMIDl93AaGZK5Hd2H5OfloGy/pg85rTnkxQwTZznb9k+cVDP86ZB6FOjV4rq+Cf1Oo3P8eH+Hk9wjd2ixgP/HPxemWiX/5iIzkW5a1ih1kF9lIpeSUlbjDXfr9rraQNbudM+N7SRTnfZr4bshtajwWOYP1INme0zMiu6ZYaW6Cs2OEllZGfJi6xDtbRMsh509rD2BVY3+ZmkUl//c+jjkqCCXsnpcH3hsTSjOJWYuLu7/yE=",
            config_file_json='templates/kubernetes/config/tanzu.json',
            config_file_yaml='templates/kubernetes/config/tanzu.yaml',
            bearer='MYSECRET',
        )

        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)
        has_resource(synthesized, "vcd_rde")


if __name__ == "__main__":
    pytest.main()
