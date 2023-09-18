import argparse
from argparse import RawTextHelpFormatter
from furl import furl

parser = argparse.ArgumentParser(description='x9', formatter_class=RawTextHelpFormatter)


def extract_params():
    parser.add_argument("-l", "--list", help="List of urls to edit", required=True)
    parser.add_argument("-p", "--parameters", help="Parameter wordlist to fuzz")
    parser.add_argument("-c", "--chunk", type=int, default=15, help="Chunk to fuzz the parameters. [default: %("
                                                                    "default)s)]")
    parser.add_argument("-v", "--value", help="Value for parameters to FUZZ", required=True)
    parser.add_argument("-gs", "--generate-strategy", choices=['normal', 'ignore', 'combine', 'all'],
                        help='''Select the mode strategy from the available choices:
    normal: Remove all parameters and the wordlist
    combine: Pitchfork combine on the existing parameters
    ignore: Don't touch the URL and put the wordlist
    all: All in one method''', required=True)
    parser.add_argument("-vs", "--value-strategy", choices=['replace', 'suffix'],
                        help='''Select the value strategy from the available choices:
    replace: Replace the value with gathered value
    suffix: Append the value to the end of the parameters''', required=True)
    parser.add_argument("-o", "--output", help="Output results")
    parser.add_argument("-d", "--debug", help="Debug mode", action='store_true')

    args = parser.parse_args()

    if args.debug:
        if args.list:
            print("Displaying List as: % s" % args.list)
        if args.parameters:
            print("Displaying Parameters as: % s" % args.parameters)
        if args.chunk:
            print("Displaying Chunk as: % s" % args.chunk)
        if args.value:
            print("Displaying Values as: % s" % args.value)
        if args.generate_strategy:
            print("Displaying generate-strategy as: % s" % args.generate_strategy)
        if args.value_strategy:
            print("Displaying value-strategy as: % s" % args.value_strategy)
        if args.output:
            print("Displaying Output as: % s" % args.output)
    return args


def get_list_urls(url_list):
    file = open(url_list, 'r')
    urls = file.readlines()
    file.close()
    return urls


def get_list_params(parameters):
    file = open(parameters, 'r')
    params = file.readlines()
    file.close()
    return params


def combine(urls, payloads, value_strategy):
    c_url = list()
    for payload in payloads:
        for url in urls:
            f = furl(url)
            f1 = furl(url)
            query_strings = dict(f.args)
            for k, v in query_strings.items():
                query_strings1 = dict(f1.args)
                if str(value_strategy) == 'suffix':
                    # print('--------------------')
                    # print('query_strings', query_strings[k])
                    if str(query_strings[k]) != 'None':     # its for && in urls - need to be fixed to support these kind of urls
                        query_strings1[k] = query_strings[k] + payload
                else:
                    if str(query_strings[k]) != 'None':
                        query_strings1[k] = payload
                f.set(args=query_strings1)
                c = str(f.url)
                f = furl(c)
                c_url.append(f.url)
    return c_url


def ignore(urls, parameters, payloads):
    c_url = list()
    params = get_list_params(parameters)

    for payload in payloads:
        all_params = ''
        for p in params:
            all_params += '&' + p.strip() + '=' + payload

        for url in urls:
            f = furl(url)
            new_params = str(f.url) + all_params
            f = furl(new_params)
            c_url.append(f.url)
    return c_url


def _all(urls, parameters, payloads, value_strategy):
    c_url = list()
    params = get_list_params(parameters)

    for payload in payloads:
        all_params = ''
        for p in params:
            all_params += '&' + p.strip() + '=' + payload
        for url in urls:
            f = furl(url)
            f1 = furl(url)
            query_strings = dict(f.args)
            for k, v in query_strings.items():
                query_strings1 = dict(f1.args)
                if str(value_strategy) == 'suffix':
                    if str(query_strings[k]) != 'None':
                        query_strings1[k] = query_strings[k] + payload
                else:
                    if str(query_strings[k]) != 'None':
                        query_strings1[k] = payload
                f.set(args=query_strings1)
                c = str(f.url) + all_params
                f = furl(c)
                c_url.append(f.url)
        for url in urls:
            f = furl(url)
            new_params = str(f.url) + all_params
            f = furl(new_params)
            c_url.append(f.url)
    return c_url


def normal(urls, parameters, payloads):
    c_url = list()
    params = ''
    params_enabled = False

    if str(parameters) != 'None':
        params = get_list_params(parameters)
        params_enabled = True

    for payload in payloads:
        all_params = ''

        if params_enabled is True:
            for p in params:
                all_params += '&' + p.strip() + '=' + payload

        for url in urls:
            f = furl(url)
            query_strings = dict(f.args)
            for k, v in query_strings.items():
                query_strings[k] = payload
            f.set(args=query_strings)
            c = str(f.url) + all_params
            f = furl(c)
            c_url.append(f.url)

    return c_url


def main():
    args = extract_params()
    url_list = args.list
    parameters = args.parameters
    chunks = args.chunk
    values = args.value
    generate_strategy = args.generate_strategy
    value_strategy = args.value_strategy
    output = args.output
    error = ''
    urls = get_list_urls(url_list)
    payloads = str(values).split(",")

    # List of crafted urls
    c_url = list()

    match str(generate_strategy):
        case 'normal':
            c_url.extend(normal(urls, parameters, payloads))
        case 'combine':
            c_url.extend(combine(urls, payloads, value_strategy))
        case 'ignore':
            if str(parameters) != 'None':
                c_url.extend(ignore(urls, parameters, payloads))
            else:
                error = "no parameters found, use -p or --parameters"
        case 'all':
            if str(parameters) != 'None':
                c_url.extend(_all(urls, parameters, payloads, value_strategy))
            else:
                error = "no parameters found, use -p or --parameters"
        case default:
            print("not supported gs provided")

    if error == '':
        for cu in c_url:
            print(cu)
    else:
        print(error)


if __name__ == '__main__':
    main()
