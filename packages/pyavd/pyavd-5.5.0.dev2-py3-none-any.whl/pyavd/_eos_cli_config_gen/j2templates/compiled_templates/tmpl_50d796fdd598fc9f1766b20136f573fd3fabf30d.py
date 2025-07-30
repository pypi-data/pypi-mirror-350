from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/platform.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_platform = resolve('platform')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='platform') if l_0_platform is missing else l_0_platform)):
        pass
        yield '\n## Platform\n'
        if ((t_3(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident')) or t_3(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'))) or t_3(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'))):
            pass
            yield '\n### Platform Summary\n'
            if t_3(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident')):
                pass
                yield '\n#### Platform Trident Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'l3'), 'routing_mac_address_per_vlan'), True):
                    pass
                    yield '| Routing MAC Address per VLAN | true |\n'
                if t_3(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'forwarding_table_partition')):
                    pass
                    yield '| Forwarding Table Partition | '
                    yield str(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'forwarding_table_partition'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'mmu'), 'active_profile')):
                    pass
                    yield '| MMU Applied Profile | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'mmu'), 'active_profile'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'mmu'), 'queue_profiles')):
                    pass
                    yield '\n#### Trident MMU QUEUE PROFILES\n'
                    for l_1_profile in t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'trident'), 'mmu'), 'queue_profiles'), 'name'):
                        _loop_vars = {}
                        pass
                        yield '\n##### '
                        yield str(environment.getattr(l_1_profile, 'name'))
                        yield '\n\n| Type | Egress Queue | Threshold | Reserved | Drop-Precedence |\n| ---- | ------------ | --------- | -------- | --------------- |\n'
                        for l_2_queue in t_2(environment.getattr(l_1_profile, 'unicast_queues'), 'id'):
                            _loop_vars = {}
                            pass
                            yield '| Unicast | '
                            yield str(environment.getattr(l_2_queue, 'id'))
                            yield ' | '
                            yield str(t_1(environment.getattr(l_2_queue, 'threshold'), '-'))
                            yield ' | '
                            yield str(t_1(environment.getattr(l_2_queue, 'reserved'), '-'))
                            yield ' '
                            yield str(t_1(environment.getattr(l_2_queue, 'unit'), 'bytes'))
                            yield ' | '
                            yield str(t_1(environment.getattr(l_2_queue, 'drop_precedence'), '-'))
                            yield ' |\n'
                        l_2_queue = missing
                        for l_2_queue in t_2(environment.getattr(l_1_profile, 'multicast_queues'), 'id'):
                            _loop_vars = {}
                            pass
                            yield '| Multicast | '
                            yield str(environment.getattr(l_2_queue, 'id'))
                            yield ' | '
                            yield str(t_1(environment.getattr(l_2_queue, 'threshold'), '-'))
                            yield ' | '
                            yield str(t_1(environment.getattr(l_2_queue, 'reserved'), '-'))
                            yield ' '
                            yield str(t_1(environment.getattr(l_2_queue, 'unit'), 'bytes'))
                            yield ' | '
                            yield str(t_1(environment.getattr(l_2_queue, 'drop_precedence'), '-'))
                            yield ' |\n'
                        l_2_queue = missing
                    l_1_profile = missing
            if t_3(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand')):
                pass
                yield '\n#### Platform Sand Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_3(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'forwarding_mode')):
                    pass
                    yield '| Forwarding Mode | '
                    yield str(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'forwarding_mode'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'hardware_only')):
                    pass
                    yield '| Hardware Only Lag | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'hardware_only'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'mode')):
                    pass
                    yield '| Lag Mode | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'lag'), 'mode'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'multicast_replication'), 'default')):
                    pass
                    yield '| Default Multicast Replication | '
                    yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'multicast_replication'), 'default'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'qos_maps')):
                    pass
                    yield '\n##### Internal Network QOS Mapping\n\n| Traffic Class | To Network QOS |\n| ------------- | -------------- |\n'
                    for l_1_qos_map in t_2(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sand'), 'qos_maps'), 'traffic_class'):
                        _loop_vars = {}
                        pass
                        if (t_3(environment.getattr(l_1_qos_map, 'traffic_class')) and t_3(environment.getattr(l_1_qos_map, 'to_network_qos'))):
                            pass
                            yield '| '
                            yield str(environment.getattr(l_1_qos_map, 'traffic_class'))
                            yield ' | '
                            yield str(environment.getattr(l_1_qos_map, 'to_network_qos'))
                            yield ' |\n'
                    l_1_qos_map = missing
            if t_3(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe')):
                pass
                yield '\n#### Platform Software Forwarding Engine Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_3(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'), 'data_plane_cpu_allocation_max')):
                    pass
                    yield '| Maximum CPU Allocation | '
                    yield str(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'), 'data_plane_cpu_allocation_max'))
                    yield ' |\n'
                if t_3(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'), 'interface')):
                    pass
                    if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'), 'interface'), 'interface_profile')):
                        pass
                        yield '| Interface profile | '
                        yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'), 'interface'), 'interface_profile'))
                        yield ' |\n'
                    if t_3(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'), 'interface'), 'profiles')):
                        pass
                        yield '\n#### Platform Software Forwarding Engine Interface Profiles\n'
                        for l_1_profile_data in t_2(environment.getattr(environment.getattr(environment.getattr((undefined(name='platform') if l_0_platform is missing else l_0_platform), 'sfe'), 'interface'), 'profiles'), 'name'):
                            _loop_vars = {}
                            pass
                            yield '\n##### '
                            yield str(environment.getattr(l_1_profile_data, 'name'))
                            yield '\n'
                            if t_3(environment.getattr(l_1_profile_data, 'interfaces')):
                                pass
                                yield '\n| Interface | Rx-Queue Count | Rx-Queue Worker | Rx-Queue Mode |\n| --------- | -------------- | --------------- | ------------- |\n'
                                for l_2_interface_data in t_2(environment.getattr(l_1_profile_data, 'interfaces'), 'name'):
                                    l_2_rx_queue_count = l_2_rx_queue_worker = l_2_rx_queue_mode = missing
                                    _loop_vars = {}
                                    pass
                                    l_2_rx_queue_count = t_1(environment.getattr(environment.getattr(l_2_interface_data, 'rx_queue'), 'count'), '-')
                                    _loop_vars['rx_queue_count'] = l_2_rx_queue_count
                                    l_2_rx_queue_worker = t_1(environment.getattr(environment.getattr(l_2_interface_data, 'rx_queue'), 'worker'), '-')
                                    _loop_vars['rx_queue_worker'] = l_2_rx_queue_worker
                                    l_2_rx_queue_mode = t_1(environment.getattr(environment.getattr(l_2_interface_data, 'rx_queue'), 'mode'), '-')
                                    _loop_vars['rx_queue_mode'] = l_2_rx_queue_mode
                                    yield '| '
                                    yield str(environment.getattr(l_2_interface_data, 'name'))
                                    yield ' | '
                                    yield str((undefined(name='rx_queue_count') if l_2_rx_queue_count is missing else l_2_rx_queue_count))
                                    yield ' | '
                                    yield str((undefined(name='rx_queue_worker') if l_2_rx_queue_worker is missing else l_2_rx_queue_worker))
                                    yield ' | '
                                    yield str((undefined(name='rx_queue_mode') if l_2_rx_queue_mode is missing else l_2_rx_queue_mode))
                                    yield ' |\n'
                                l_2_interface_data = l_2_rx_queue_count = l_2_rx_queue_worker = l_2_rx_queue_mode = missing
                        l_1_profile_data = missing
        yield '\n### Platform Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/platform.j2', 'documentation/platform.j2')
        gen = template.root_render_func(template.new_context(context.get_all(), True, {}))
        try:
            for event in gen:
                yield event
        finally: gen.close()
        template = environment.get_template('eos/platform-sfe-interface.j2', 'documentation/platform.j2')
        gen = template.root_render_func(template.new_context(context.get_all(), True, {}))
        try:
            for event in gen:
                yield event
        finally: gen.close()
        yield '```\n'

blocks = {}
debug_info = '7=30&10=33&13=36&19=39&22=42&23=45&25=47&26=50&28=52&31=55&33=59&37=61&38=65&40=76&41=80&46=92&52=95&53=98&55=100&56=103&58=105&59=108&61=110&62=113&64=115&70=118&71=121&72=124&77=129&83=132&84=135&87=137&88=139&89=142&91=144&94=147&96=151&97=153&101=156&102=160&103=162&104=164&105=167&117=178&118=184'