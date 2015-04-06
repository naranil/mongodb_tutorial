# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    #results = query_by_name(ARTIST_URL, query_type["simple"], "Metallica")
    #pretty_print(results)
    #artist_id = results["artists"][0]["id"]
    #print "\nARTIST:"
    #pretty_print(results["artists"][1])

    #artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    #releases = artist_data["releases"]
    #print "\nONE RELEASE:"
    #pretty_print(releases[0], indent=2)
    #release_titles = [r["title"] for r in releases]

    #print "\nALL TITLES:"
    #for t in release_titles:
    #    print t

    ## Question answers:
    #
    #
    print '1- How many bands named named "First Aid Kit" ? \n'
    results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    nb_artists=0
    for artist in results["artists"]:
        if artist["score"] == '100':
            print artist["name"]
            nb_artists += 1
    print "Nb of bands called First Aid Kit ", nb_artists , '\n'

    #
    #
    #
    print  '2- Begin-area name for Queen \n'
    results = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    print "Begin-area name for Queen, ", results["artists"][0]["begin-area"]["name"], '\n'
    #
    #
    #
    print '3- Spanish alias for beatles ? \n'
    results = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    aliases = results["artists"][0]["aliases"]
    for name in aliases:
        if name["locale"] == 'es':
            print "Spanish name of the Beatles ", name["name"]
    print '\n'
    #
    #
    #
    print '4- Nirvana disambiguation \n'
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    print results["artists"][0]["disambiguation"]
    print '\n'
    #
    #
    #
    print '5- When was one direction formed \n'
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    print results["artists"][0]["disambiguation"]
main()
#if __name__ == '__main__':












#    main()