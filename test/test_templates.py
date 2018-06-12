
import yaml
from jinja2 import FileSystemLoader, Environment
import ansible.plugins.filter.core
from datetime import datetime
import pytest

# set up applicable ansible yaml filters
env = Environment(loader=FileSystemLoader('templates'))
env.filters['to_nice_yaml'] = ansible.plugins.filter.core.to_nice_yaml

# set up a fake ansible fact for the current date
# it's needed in the templates for "last changed" dates
ansible_date_time = lambda: None
ansible_date_time.iso8601 = datetime.now().isoformat()

# load template
template = env.get_template('metricbeat.j2')

def test_defaults():
    # load vars from defaults/main.yml
    with open('defaults/main.yml') as f:
        defaults = yaml.load(f.read())

    defaults.update({'ansible_date_time': ansible_date_time})

    # render template to yaml
    result_yaml = template.render(**defaults)
    result_obj = yaml.load(result_yaml)

    # check that defaults are present
    assert result_obj['metricbeat.config.modules']['path'] == "{}/modules.d/*.yml".format(defaults['metricbeat_configs_path'])
    assert result_obj['setup.kibana']['host'] == defaults['metricbeat_setup_kibana_host']
    assert result_obj['output.elasticsearch']['hosts'] == defaults['metricbeat_output_elasticsearch_hosts']
    assert result_obj['logging.level'] == defaults['metricbeat_logging_level']
    assert result_obj['logging.selectors'] == defaults['metricbeat_logging_selectors']
    assert result_obj['xpack.monitoring.enabled'] == defaults['metricbeat_xpack_monitoring']

    # check that optional keys are not present
    # slightly backwards logic: loop reports True if the key is NOT present.
    # so we want to confirm that ALL return vals are True
    # alternative would be `not any([True if ... else False...])` which seems less readable
    optional_keys = ['name', 'tags', 'fields', 'cloud.id', 'cloud.auth',
                    'output.logstash', 'xpack.monitoring.elasticsearch']
    assert all([False if k in result_obj.keys() else True for k in optional_keys])


def test_optional_settings():
    # load vars from tests/optional_settings.yml
    with open('test/optional_settings.yml') as f:
        optional_settings = yaml.load(f.read())
    optional_settings.update({'ansible_date_time': ansible_date_time})

    # render template to yaml
    result_yaml = template.render(**optional_settings)
    result_obj = yaml.load(result_yaml)

    # check that the new settings are present
    assert result_obj['metricbeat.config.modules']['path'] == "{}/modules.d/*.yml".format(optional_settings['metricbeat_configs_path'])
    assert result_obj['setup.kibana']['host'] == optional_settings['metricbeat_setup_kibana_host']
    assert result_obj['name'] == optional_settings['metricbeat_name']
    assert result_obj['tags'] == optional_settings['metricbeat_tags']
    assert result_obj['fields'] == optional_settings['metricbeat_fields']
    assert result_obj['cloud.id'] == optional_settings['metricbeat_elastic_cloud_id']
    assert result_obj['cloud.auth'] == optional_settings['metricbeat_elastic_cloud_auth']
    assert result_obj['output.elasticsearch']['hosts'] == optional_settings['metricbeat_output_elasticsearch_hosts']
    assert result_obj['output.elasticsearch']['protocol'] == optional_settings['metricbeat_output_elasticsearch_protocol']
    assert result_obj['output.elasticsearch']['username'] == optional_settings['metricbeat_output_elasticsearch_username']
    assert result_obj['output.elasticsearch']['password'] == optional_settings['metricbeat_output_elasticsearch_password']
    assert result_obj['output.logstash']['hosts'] == optional_settings['metricbeat_output_logstash_hosts']
    assert result_obj['output.logstash']['ssl.certificate_authorities'] == optional_settings['metricbeat_output_logstash_ssl_ca']
    assert result_obj['output.logstash']['ssl.certificate'] == optional_settings['metricbeat_output_logstash_ssl_cert']
    assert result_obj['output.logstash']['ssl.key'] == optional_settings['metricbeat_output_logstash_ssl_key']
    assert result_obj['logging.level'] == optional_settings['metricbeat_logging_level']
    assert result_obj['logging.selectors'] == optional_settings['metricbeat_logging_selectors']
    assert result_obj['xpack.monitoring.enabled'] == optional_settings['metricbeat_xpack_monitoring']
    assert result_obj['xpack.monitoring.elasticsearch'] == optional_settings['metricbeat_xpack_monitoring_elasticsearch_config']

