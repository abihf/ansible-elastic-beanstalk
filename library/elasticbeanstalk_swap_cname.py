#!/usr/bin/env python

DOCUMENTATION = '''
---
module: elasticbeanstalk_swap_cname
short_description: swap environment cname
description:
    - swap environment cname

options:
  source_environment:
    description:
      - name of source environment
    required: true
  destination_environment:
    description:
      - name of destination environment
    required: true
author: Abi Hafshin
extends_documentation_fragment: aws
'''

EXAMPLES = '''
# Create or update an application
- elasticbeanstalk_swap_cname:
    app_name: Sample App
    source_environment: blue-environment
    destination_environment: green-environment
'''

RETURN = '''
output:
    description: message indicating what change will occur
    returned: in check mode
    type: string
    sample: App is up-to-date
'''


try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info

def filter_empty(**kwargs):
    return {k:v for k,v in kwargs.items() if v}

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
            source_environment      = dict(type='str', required=True),
            destination_environment = dict(type='str', required=True)
        ),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    if not HAS_BOTO3:
        module.fail_json(msg='boto3 required for this module')

    source_environment = module.params['source_environment']
    destination_environment = module.params['destination_environment']

    result = {}
    region, ec2_url, aws_connect_params = get_aws_connection_info(module, boto3=True)

    if region:
        eb = boto3_conn(module, conn_type='client', resource='elasticbeanstalk',
                region=region, endpoint=ec2_url, **aws_connect_params)
    else:
        module.fail_json(msg='region must be specified')

    if module.check_mode:
        # check_app(ebs, app, module)
        module.fail_json(msg='ASSERTION FAILURE: check_app() should not return control.')

    eb.swap_environment_cnames(**filter_empty(SourceEnvironmentName=source_environment,
                                              DestinationEnvironmentName=destination_environment))
    module.exit_json(changed=True)

if __name__ == '__main__':
    main()
