# Metricbeat

An Ansible role for installing Elastic's Metricbeat on RHEL- or Debian-based hosts.

## Requirements

None

## Role Variables

See [`defaults/main.yml`](defaults/main.yml). Vars are well-commented and mirror the Metricbeat config options pretty closely.

The module config defaults are exactly what's used in the default `metricbeat.yml` config installed with the rest of the official packages.

## Usage

1. Provide `metricbeat_module_configs_enabled` with a list of enabled metrics-gathering modules. `system` is enabled and configured sanely by default.

2. Provide `metricbeat_module_configs` with a dictionary where each key is a module name and each value is a list of dictionaries loaded with config options. See the [docs](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-modules.html) for more information on configuring modules.

3. Set up Logstash and/or Elasticsearch outputs using `metricbeat_output_logstash_hosts` and/or `metricbeat_output_elasticsearch_hosts`. SSL and auth can be configured, see [`defaults/main.yml`](defaults/main.yml) for more information.

4. By default, the role will attempt to set up Elasticsearch indexes, ML features, and Kibana dashboards. To prevent this, set `metricbeat_setup_run` to `False`.

5. Run your playbook.

## Testing

* [`requirements_dev.txt`](requirements_dev.txt) contains all the Python deps for testing. Nothing too shocking in here.
* `pytest` is used to test template logic, see `test/test_templates.py` for more information. Run it using `python -m pytest` from the repo directory.
* `test.yml` requires an Elasticsearch and Kibana nodes present on `localhost` by default. See [`.gitlab-ci.yml`](.gitlab-ci.yml) or [`.travis.yml`](.travis.yml) for examples of testing with Docker.

## License

BSD

