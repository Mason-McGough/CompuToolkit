class OpNet:
    pass

class Node:
    class Conduit:
        last_value = None

    class Param(Conduit):
        def __init__(self, name, source=None, datatypes=(None,)):
            self.name = name
            self.source = source

            datatypes = ensure_is_listlike(datatypes)
            self.datatypes = datatypes

    class Output(Conduit):
        def __init__(self, name, output=None, datatypes=(None,)):
            self.name = name
            self.output = output

            datatypes = ensure_is_listlike(datatypes)
            self.datatypes = datatypes

    def __init__(self, op, params, outputs):
        """
        Create new node.

        Inputs:
            op: Reference to function.
            params: Dictionary of parameters to function defined in 'op'. The key 
                is the name of the parameter and the value is its assigned value.
            outputs: List of strings with arbitrary names for ordered outputs of 
                function 'op'.
        """

        # init op
        self.op = op

        # init params
        self.params = [Node.Param(name, value) for (name, value) in params.items()]

        # init outputs
        self.outputs = [Node.Output(name) for name in outputs]

    def __repr__(self):
        return "<Node op:{0} params:{1} outputs:{2}>".format(self.op, self.params, self.outputs)

    def __str__(self):
        return "Node: \
                    \n\top: {0} \
                    \n\tparams: {1} \
                    \n\toutputs: {2}".format(self.op, self.params, self.outputs)

    def unpack_params(self):
        """
        Return dict of params with key as name and source as value.
        """

        return {param.name: param.source for param in self.params}

    def list_outputs(self):
        """
        Return list of output names.
        """

        return [output.name for output in self.outputs]

    def param_values(self):
        return {param.name: param.last_value for param in self.params}

    def output_values(self):
        return {output.name: output.last_value for output in self.outputs}

    def execute(self):
        outs = self.op(**self.unpack_params())
        outs = ensure_is_listlike(outs)

        # store outputs as last_value
        for (s_out, out) in zip(self.outputs, outs):
            s_out.last_value = out

        # convert to dict for output
        outs = {name: out for (name, out) in zip(self.list_outputs(), outs)}
        return outs

def ensure_is_listlike(thing):
    if not isinstance(thing, (list, tuple)):
        thing = [thing,]

    return thing

def _call_ops(data, ops_names, ops_params):
    """
    Sequentially run DATA through all functions in list OPS_NAMES using the 
    parameters in list OPS_PARAMS.
    """

    ops = [
        {'op': getattr(htk, op_name),
         'op_name': op_name,
         'params': params
        } for op_name, params in zip(ops_names, ops_params)
    ]

    ops_output = []
    for op in ops:
        op_output = op['op'](data, **op['params'])
        ops_output.append(op_output)

        if 'data' in op_output:
            data = op_output['data']

    return data, ops_output