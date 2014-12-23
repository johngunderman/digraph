


def arg_binded_gcl_execute(query, **args):
    """Execute a GQL query after binding optional numbered args.

    GQL Arguments are provided in numeric form, eg @1 or @2, etc.

    Example Query String:
      'SELECT * FROM Person WHERE height >= @1 AND height <= @2'

    Returns:
      The results of the query as a list of entities
    """
    req = datastore.RunQueryRequest()
    gql_query = req.gql_query
    gql_query.query_string = query

    for arg in args:
        if type(arg) is str:
            gql_query.number_arg.add().value.string_value = arg
        if type(arg) is int:
            gql_query.number_arg.add().value.integer_value = arg

    resp = self.datastore.run_query(req)
    results = [entity_result.entity
            for entity_result in resp.batch.entity_result]
    return results
