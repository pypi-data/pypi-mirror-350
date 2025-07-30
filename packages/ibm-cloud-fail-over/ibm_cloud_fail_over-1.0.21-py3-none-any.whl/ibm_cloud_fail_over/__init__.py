"""IBM Cloud Fail Over package."""

from .ibm_cloud_fail_over import (
    HAFailOver,
    fail_over_cr_vip,
    fail_over_floating_ip_start,
    fail_over_floating_ip_stop,
    fail_over_get_attached_fip,
    fail_over_public_address_range,
    fail_over_check_par_zone_compatibility,
    get_next_hop_for_par,
    fail_over_check_next_hop_internet_ingress,
)

__all__ = [
    'HAFailOver',
    'fail_over_cr_vip',
    'fail_over_floating_ip_start',
    'fail_over_floating_ip_stop',
    'fail_over_get_attached_fip',
    'fail_over_public_address_range',
    'fail_over_check_par_zone_compatibility',
    'get_next_hop_for_par',
    'fail_over_check_next_hop_internet_ingress',
]
