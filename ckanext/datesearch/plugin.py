import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)


class DateSearchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'ckanext-datesearch')

    def before_search(self, search_params):
        extras = search_params.get('extras')
        log.debug("extras: {0}".format(extras))
        if not extras:
            # There are no extras in the search params, so do nothing.
            return search_params

        start_date = extras.get('ext_startdate')
        log.debug("start_date: {0}".format(start_date))

        end_date = extras.get('ext_enddate')
        log.debug("end_date: {0}".format(end_date))

        if not start_date and not end_date:
            # The user didn't select either a start and/or end date, so do nothing.
            return search_params
        if not start_date:
            start_date = '*'
        if not end_date:
            end_date = '*'

        # Add a date-range query with the selected start and/or end dates into the Solr facet queries.
        fq = search_params['fq']
        log.debug("fq: {0}".format(fq))
        fq = '{fq} +(temporal-extent-begin:[* TO {ed}] and temporal-extent-end:[{sd} TO * ])'.format(fq=fq, sd=start_date, ed=end_date)

        log.debug("fq: {0}".format(fq))
        search_params['fq'] = fq
        log.debug("search_params: {0}".format(search_params))

        return search_params
