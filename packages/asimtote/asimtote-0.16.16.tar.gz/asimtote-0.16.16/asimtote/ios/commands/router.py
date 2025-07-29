# asimtote.ios.commands.router
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault
import netaddr

from ..utils import interface_canonicalize, VRF_GLOBAL
from ...config import IndentedContextualCommand



# --- functions ---



def neighbor_canonicalize(nbr):
    """Canonicalise a BGP neighbor identifier - these can be descriptive
    names (for a peer-group) or an IP address.  In the case of IPv6, we
    need to ensure the case is consistent, so we upper case it.

    If the name is not an IPv6 address, we return it as-is.
    """

    if netaddr.valid_ipv6(nbr):
        return str(netaddr.IPAddress(nbr, 6)).upper()

    return nbr



# --- configuration command classes ---



# =============================================================================
# ip[v6] route ...
# =============================================================================



class Cmd_IPRoute(IndentedContextualCommand):
    match = (r"ip route( vrf (?P<vrf>\S+))? (?P<base>\S+) (?P<netmask>\S+)"
             r"( (?P<int_name>[-A-Za-z]+[0-9/.]+))?( (?P<router>[0-9.]+))?"
             r"( (?P<metric1>\d+))?( tag (?P<tag>\d+))?( (?P<metric2>\d+))?")

    def parse(self, cfg, vrf, base, netmask, int_name, router, metric1, tag,
              metric2):
        # get a canonical form of the destination network and interface name
        net = str(netaddr.IPNetwork(base + '/' + netmask))
        int_name = interface_canonicalize(int_name) if int_name else None

        # build a unique hashable indentifier for the next hop of this
        # route (i.e. interface and router address, if available)
        #
        # the actual contents are not important (although can be used in
        # a rule) but are needed to determine which routes are being
        # added, removed and changed (in terms of metric, tag, etc.) by
        # comparing the identifiers
        id = (int_name or '-') + ' ' + (router or '-')

        r = {}
        if int_name:
            r["interface"] = int_name
        if router:
            r["router"] = router
        if metric1 or metric2:
            r["metric"] = int(metric1 or metric2)
        if tag:
            r["tag"] = int(tag)

        deepsetdefault(cfg, "ip-route", vrf, net)[id] = r


class Cmd_IPv6Route(IndentedContextualCommand):
    match = (r"ipv6 route( vrf (?P<vrf>\S+))? (?P<net>\S+)"
             r"( (?P<int_name>[-A-Za-z]+[0-9/.]+))?( (?P<router>[0-9a-f:]+))?"
             r"( (?P<metric1>\d+))?( tag (?P<tag>\d+))?( (?P<metric2>\d+))?")

    def parse(self, cfg, vrf, net, int_name, router, metric1, tag, metric2):
        net = str(netaddr.IPNetwork(net))
        router = str(netaddr.IPAddress(router)) if router else None
        int_name = interface_canonicalize(int_name) if int_name else None

        id = (int_name or '-') + ' ' + (router or '-')

        r = {}
        if int_name:
            r["interface"] = int_name
        if router:
            r["router"] = router
        if metric1 or metric2:
            r["metric"] = int(metric1 or metric2)
        if tag:
            r["tag"] = int(tag)

        deepsetdefault(cfg, "ipv6-route", vrf, net)[id] = r



# =============================================================================
# route-map ...
# =============================================================================



class Cmd_RtMap(IndentedContextualCommand):
    match = (r"route-map (?P<rtmap>\S+)( (?P<action>permit|deny))?"
             r"( (?P<seq>\d+))?")
    enter_context = "route-map"

    def parse(self, cfg, rtmap, action, seq):
        # if the sequence number is omitted, the route-map must either
        # be empty, in which case 10 is assumed, or have only one entry,
        # in which case that entry is modified

        if seq is None:
            if len(r) > 1:
                raise ValueError("route-map without sequence number and "
                                 "multiple existing entries")

            seq = 10 if len(r) == 0 else r[0]

        r = deepsetdefault(cfg, "route-map", rtmap, int(seq))

        # if no action is specified, 'permit' is assumed
        r["action"] = action or "permit"

        return r


class CmdContext_RtMap(IndentedContextualCommand):
    context = "route-map"


class Cmd_RtMap_MatchCmty(CmdContext_RtMap):
    match = r"match community (?P<cmtys>.+?)(?P<exact> exact-match)?"

    def parse(self, cfg, cmtys, exact):
        m = deepsetdefault(cfg, "match", "community")
        m.setdefault("communities", set()).update(cmtys.split(' '))
        if exact:
            m["exact-match"] = True


class Cmd_RtMap_MatchIPAddr(CmdContext_RtMap):
    match = r"match ip address(?P<pfx> prefix-list)? (?P<addrs>.+?)"

    def parse(self, cfg, pfx, addrs):
        # matching IP addresses can either be done by access-list (the
        # default) or prefix-list, but not both and one type cannot
        # directly be changed to another
        m = deepsetdefault(cfg, "match",
                           "ip-prefix-list" if pfx else "ip-address",
                           last=set())

        m.update(addrs.split(' '))


class Cmd_RtMap_MatchIPv6Addr(CmdContext_RtMap):
    match = r"match ipv6 address(?P<pfx> prefix-list)? (?P<addrs>.+?)"

    def parse(self, cfg, pfx, addrs):
        m = deepsetdefault(cfg, "match",
                           "ipv6-prefix-list" if pfx else "ipv6-address",
                           last=set())

        m.update(addrs.split(' '))


class Cmd_RtMap_MatchTag(CmdContext_RtMap):
    match = r"match tag (?P<tags>.+)"

    def parse(self, cfg, tags):
        m = deepsetdefault(cfg, "match", "tag", last=set())
        m.update(int(t) for t in tags.split(' '))


class Cmd_RtMap_SetCmty(CmdContext_RtMap):
    match = r"set community (?P<cmtys>.+?)(?P<add> additive)?"

    def parse(self, cfg, cmtys, add):
        s = deepsetdefault(cfg, "set", "community")
        s.setdefault("communities", set()).update(cmtys.split(' '))
        if add:
            s["additive"] = True


class Cmd_RtMap_SetIPNxtHop(CmdContext_RtMap):
    match = (r"set ip((?P<_global> global)| vrf (?P<vrf>\S+))? "
             r"next-hop (?P<addrs>[0-9. ]+)")

    def parse(self, cfg, _global, vrf, addrs):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        l = deepsetdefault(cfg, "set", "ip-next-hop", last=[])
        for addr in addrs.split(' '):
            nexthop = { "addr": addr }
            if _global or vrf:
                # the 'vrf' key is set if 'global' or a VRF is
                # specified for the next hop - if to global, the empty
                # string is used (we could use None but we're being
                # consistent with 'set global')
                nexthop["vrf"] = vrf or ""
            l.append(nexthop)


class Cmd_RtMap_SetIPNxtHopVrfy(CmdContext_RtMap):
    match = r"set ip next-hop verify-availability"

    def parse(self, cfg):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        deepsetdefault(cfg, "set")["ip-next-hop-verify-availability"] = True


class Cmd_RtMap_SetIPNxtHopVrfyTrk(CmdContext_RtMap):
    match = (r"set ip next-hop verify-availability (?P<addr>[0-9.]+) "
             r"(?P<seq>\d+) track (?P<obj>\d+)")

    def parse(self, cfg, addr, seq, obj):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        v = deepsetdefault(cfg, "set", "ip-next-hop-verify-availability-track")
        v[int(seq)] = {
            "addr": addr,
            "track-obj": int(obj)
        }


class Cmd_RtMap_SetIPv6NxtHop(CmdContext_RtMap):
    match = r"set ipv6 next-hop (?P<addrs>[0-9a-f: ]+)"

    def parse(self, cfg, addrs):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        l = deepsetdefault(cfg, "set", "ipv6-next-hop", last=[])
        for addr in addrs.split(' '):
            # we don't really need to use a dictionary here, but it
            # keeps it consistent with the IPv4 version, in case extra
            # options are added in future
            l.append({ "addr": addr })


class Cmd_RtMap_SetLocalPref(CmdContext_RtMap):
    match = r"set local-preference (?P<pref>\d+)"

    def parse(self, cfg, pref):
        cfg.setdefault("set", {})["local-preference"] = int(pref)


class Cmd_RtMap_SetVRF(CmdContext_RtMap):
    # this handles both 'set global' and 'set vrf ...'
    match = r"set (global|vrf (?P<vrf>\S+))"

    def parse(self, cfg, vrf):
        # the global routing table is indicated by an empty string VRF
        # setting
        deepsetdefault(cfg, "set", "vrf", last=vrf or "")



# =============================================================================
# router bgp ...
# =============================================================================



class Cmd_RtrBGP(IndentedContextualCommand):
    # ASNs can be in 'n' as well as 'n.n' format so we can't just use an
    # integer
    match = r"router bgp (?P<asn>\d+(\.\d+)?)"
    enter_context = "router-bgp"

    def parse(self, cfg, asn):
        return deepsetdefault(cfg, "router", "bgp", asn)


class CmdContext_RtrBGP(IndentedContextualCommand):
    context = "router-bgp"


class Cmd_RtrBGP_BGPRtrID(CmdContext_RtrBGP):
    match = r"bgp router-id (?P<id>\S+)"

    def parse(self, cfg, id):
        cfg["router-id"] = id


class Cmd_RtrBGP_NbrFallOver_BFD(CmdContext_RtrBGP):
    match = (r"neighbor (?P<nbr>\S+) fall-over bfd"
             r"( (?P<bfd>single-hop|multi-hop))?")

    def parse(self, cfg, nbr, bfd):
        deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                           "fall-over")["bfd"] = bfd


class Cmd_RtrBGP_NbrFallOver_Route(CmdContext_RtrBGP):
    match = (r"neighbor (?P<nbr>\S+) fall-over"
             r"( route-map (?P<rtmap>\S+))?")

    def parse(self, cfg, nbr, rtmap):
        r = deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                               "fall-over", "route")
        if rtmap:
            r["route-map"] = rtmap


class Cmd_RtrBGP_NbrPwd(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) password( (?P<enc>\d)) (?P<pwd>\S+)"

    def parse(self, cfg, nbr, enc, pwd):
        deepsetdefault(
            cfg["neighbor"][neighbor_canonicalize(nbr)])["password"] = {
                "encryption": int(enc), "password": pwd
            }


class Cmd_RtrBGP_NbrPrGrp(CmdContext_RtrBGP):
    # this class matches the creation of a peer-group
    match = r"neighbor (?P<nbr>\S+) peer-group"

    def parse(self, cfg, nbr):
        # this creates a neighbor as a peer-group
        #
        # unlike most commands that configure neighbors and require them
        # to exist (by using 'cfg["neighbor"][...(nbr)]), this will
        # create a new neighbor using a path with deepsetdefault()
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["type"] = "peer-group"


class Cmd_RtrBGP_NbrPrGrpMbr(CmdContext_RtrBGP):
    # this class matches the addition of a member to a peer-group
    match = r"neighbor (?P<nbr>\S+) peer-group (?P<grp>\S+)"

    def parse(self, cfg, nbr, grp):
        # this creates a neighbor as a member of a peer-group
        #
        # unlike most commands that configure neighbors and require them
        # to exist (by using 'cfg["neighbor"][...(nbr)]), this will
        # create a new neighbor using a path with deepsetdefault()
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["peer-group"] = grp


class Cmd_RtrBGP_NbrRemAS(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) remote-as (?P<rem_asn>\d+(\.\d+)?)"

    def parse(self, cfg, nbr, rem_asn):
        # this creates a new neighbor host
        #
        # unlike most commands that configure neighbors and require them
        # to exist (by using 'cfg["neighbor"][...(nbr)]), this will
        # create a new neighbor using a path with deepsetdefault()
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["remote-as"] = rem_asn


class Cmd_RtrBGP_NbrUpdSrc(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) update-source (?P<int_name>\S+)"

    def parse(self, cfg, nbr, int_name):
        deepsetdefault(
            cfg["neighbor"][neighbor_canonicalize(nbr)])["update-source"] = (
                int_name)



# =============================================================================
# router bgp ... address-family ... [vrf ...]
# =============================================================================



class Cmd_RtrBGP_AF(CmdContext_RtrBGP):
    # this regexp will match 'vpnv[46] vrf ...' which is illegal, but we're
    # not trying to validate commands
    match = (r"address-family (?P<af>ipv[46]( (?P<cast>unicast|multicast))?|"
             r"vpnv4|vpnv6)( vrf (?P<vrf>\S+))?")

    enter_context = "router-bgp-af"

    def parse(self, cfg, af, cast, vrf):
        # unicast/multicast is optional - if omitted, we assume unicast
        if not cast:
            af += " unicast"

        # we put addres families in the global routing table in a VRF
        # called VRF_GLOBAL
        return deepsetdefault(
                   cfg, "vrf", vrf or VRF_GLOBAL, "address-family", af)


class CmdContext_RtrBGP_AF(IndentedContextualCommand):
    context = "router-bgp-af"


class Cmd_RtrBGP_AF_NbtAct(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) activate"

    def parse(self, cfg, nbr):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["activate"] = True


class Cmd_RtrBGP_AF_NbrAddPath(CmdContext_RtrBGP_AF):
    # 'receive' must come after 'send'; 'disable' exclusive
    match = (r"neighbor (?P<nbr>\S+) additional-paths"
             r"(( (?P<snd>send))?( (?P<rcv>receive))?|( (?P<dis>disable)))")

    def parse(self, cfg, nbr, snd, rcv, dis):
        # additional paths is a set of all matching types (or 'disable')
        deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))[
            "additional-paths"] = { a for a in (snd, rcv, dis) if a }


class Cmd_RtrBGP_AF_NbrAdvAddPath(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) advertise additional-paths"
             r"(?=.*\s(?P<all>all))?"
             r"(?=.*\s(best( (?P<best_n>\d+))))?"
             r"(?=.*\s(?P<grp_best>group-best))?"
             r".+")

    def parse(self, cfg, nbr, all, best_n, grp_best):
        a = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr),
                           "advertise-additional-paths")

        if all:
            a["all"] = True
        if best_n:
            a["best"] = int(best_n)
        if grp_best:
            a["group-best"] = True


class Cmd_RtrBGP_AF_NbrAlwAS(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) allowas-in( (?P<max>\d+))?"

    def parse(self, cfg, nbr, max):
        # we can't just use None for an empty 'allowas-in' maximum as
        # this cannot be changed to, as a different type
        n = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))
        a = {}
        if max is not None:
            a["max"] = int(max)
        n["allowas-in"] = a


class Cmd_RtrBGP_AF_NbrFallOver_BFD(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) fall-over bfd"
             r"( (?P<bfd>single-hop|multi-hop))?")

    def parse(self, cfg, nbr, bfd):
        deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                           "fall-over")["bfd"] = bfd


class Cmd_RtrBGP_AF_NbrFallOver_Route(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) fall-over"
             r"( route-map (?P<rtmap>\S+))?")

    def parse(self, cfg, nbr, rtmap):
        r = deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                               "fall-over", "route")
        if rtmap:
            r["route-map"] = rtmap


class Cmd_RtrBGP_AF_NbrFltLst(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) filter-list (?P<list_>\d+)"
             r" (?P<dir_>in|out)")

    def parse(self, cfg, nbr, list_, dir_):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr), "filter-list")[
                dir_] = int(list_)


class Cmd_RtrBGP_AF_NbrMaxPfx(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) maximum-prefix (?P<max>\d+)"
             r"( (?P<thresh>\d+))?")

    def parse(self, cfg, nbr, max, thresh):
        m = deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr), "maximum-prefix")
        m["max"] = int(max)
        if thresh:
            m["threshold"] = int(thresh)


class Cmd_RtrBGP_AF_NbrNHSelf(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) next-hop-self(?P<all> all)?"

    def parse(self, cfg, nbr, all):
        n = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))
        h = {}
        if all:
            h["all"] = True
        n["next-hop-self"] = h


class Cmd_RtrBGP_AF_NbrPrGrp(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) peer-group"

    def parse(self, cfg, nbr):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["type"] = "peer-group"


class Cmd_RtrBGP_AF_NbrPrGrpMbr(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) peer-group (?P<grp>\S+)"

    def parse(self, cfg, nbr, grp):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["peer-group"] = grp


class Cmd_RtrBGP_AF_NbrPfxLst(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) prefix-list (?P<list_>\S+)"
             r" (?P<dir_>in|out)")

    def parse(self, cfg, nbr, list_, dir_):
        deepsetdefault(cfg, "neighbor", nbr, "prefix-list")[dir_] = list_


class Cmd_RtrBGP_AF_NbrPwd(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) password( (?P<enc>\d)) (?P<pwd>\S+)"

    def parse(self, cfg, nbr, enc, pwd):
        deepsetdefault(
            cfg["neighbor"][neighbor_canonicalize(nbr)])["password"] = {
                "encryption": int(enc), "password": pwd
            }


class Cmd_RtrBGP_AF_NbrRemAs(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) remote-as (?P<rem_asn>\d+(\.\d+)?)"

    def parse(self, cfg, nbr, rem_asn):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["remote-as"] = rem_asn


class Cmd_RtrBGP_AF_NbrRemPrivAS(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) remove-private-as(?P<all> all)?"

    def parse(self, cfg, nbr, all):
        n = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))
        r = {}
        if all:
            r["all"] = True
        n["remove-private-as"] = r


class Cmd_RtrBGP_AF_NbrRtMap(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) route-map (?P<rtmap>\S+) (?P<dir_>in|out)"

    def parse(self, cfg, nbr, rtmap, dir_):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr), "route-map")[dir_] = (
                rtmap)


class Cmd_RtrBGP_AF_NbrSndCmty(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) send-community"
             r"( (?P<cmty>standard|extended|both))?")

    def parse(self, cfg, nbr, cmty):
        # this command adjusts the current state of the setting rather
        # than replacing it (e.g. entering "extended" when only
        # "standard" is set will change to "both")
        #
        # we don't worry about that but track each setting independently
        c = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr),
                           "send-community", last=set())
        if cmty in (None, "standard", "both"):
            c.add("standard")
        if cmty in ("extended", "both"):
            c.add("extended")


class Cmd_RtrBGP_AF_NbrSoftRecfg(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) soft-reconfiguration inbound"

    def parse(self, cfg, nbr):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))[
                "soft-reconfiguration"] = "inbound"


class Cmd_RtrBGP_AF_MaxPaths(CmdContext_RtrBGP_AF):
    match = r"maximum-paths (?P<paths>\d+)"

    def parse(self, cfg, paths):
        cfg["maximum-paths"] = int(paths)


class Cmd_RtrBGP_AF_MaxPathsIBGP(CmdContext_RtrBGP_AF):
    match = r"maximum-paths ibgp (?P<paths>\d+)"

    def parse(self, cfg, paths):
        cfg["maximum-paths-ibgp"] = int(paths)


class Cmd_RtrBGP_AF_Redist_Plain(CmdContext_RtrBGP_AF):
    match = (r"redistribute (?P<proto>static|connected)"
             r"( route-map (?P<rtmap>\S+))?( metric (?P<met>\d+))?")

    def parse(self, cfg, proto, rtmap, met):
        r = deepsetdefault(cfg, "redistribute", proto)
        if rtmap:
            r["route-map"] = rtmap
        if met:
            r["metric"] = int(met)


class Cmd_RtrBGP_AF_Redist_OSPF(CmdContext_RtrBGP_AF):
    match = (r"redistribute (?P<proto>ospf|ospfv3) (?P<proc>\d+)"
             r"( route-map (?P<rtmap>\S+))?( metric (?P<met>\d+))?")

    def parse(self, cfg, proto, proc, rtmap, met):
        r = deepsetdefault(cfg, "redistribute", proto, int(proc))
        if rtmap:
            r["route-map"] = rtmap
        if met:
            r["metric"] = int(met)



# =============================================================================
# router ospf ...
# =============================================================================



# this function is used for both ospf and ospfv3 so is shared

def _ospf_passive_interface(cfg, int_name, passive):
    """This function maintains a "passive-interface" dictionary under
    the supplied configuration (cfg) for OSPF or an OSPFv3 address
    family.

    The named interface (int_name) is set to either passive or active.

    If the interface name is the literal "default" then the default
    interface status is changed.
    """

    # create the "passive-interface" dictionary, if it doesn't exist
    p = cfg.setdefault("passive-interface", {})


    if int_name == "default":
        # we're changing the default

        if passive:
            # we're making passive interfaces the default so we don't
            # need to keep a list of passive interfaces, if there is one
            p["default"] = True
            if "interface" in p:
                p.pop("interface")
        else:
            # the opposite of the above
            if "default" in p:
                p.pop("default")
            if "no-interface" in p:
                p.pop("no-interface")

    else:
        # we're changing an individual interface

        # the name of the set of interfaces we're adjusting depends on
        # whether this interface is being configured as passive or
        # active
        int_set_key = "interface" if passive else "no-interface"

        ic = interface_canonicalize(int_name)
        if passive != p.get("default", False):
            # we're setting an interface state to the opposite of the
            # default - add it to the exception list
            deepsetdefault(p, int_set_key, last=set()).add(ic)

        else:
            # we're setting an interface to the same state as the
            # default - remove it from the exception set, if it exists
            if int_set_key in p:
                p[int_set_key].discard(ic)

                # if the set is now empty, we remove it completely
                if not p.get(int_set_key):
                    p.pop(int_set_key)


    # if the passive interface configuration is now empty (which means
    # we have active interfaces by default with no exceptions), remove
    # the whole passive interface configuration dictionary
    if not p:
        cfg.pop("passive-interface")



class Cmd_RtrOSPF(IndentedContextualCommand):
    match = r"router ospf (?P<proc>\d+)"
    enter_context = "router-ospf"

    def parse(self, cfg, proc):
        return deepsetdefault(cfg, "router", "ospf", int(proc))


class CmdContext_RtrOSPF(IndentedContextualCommand):
    context = "router-ospf"


class Cmd_RtrOSPF_ID(CmdContext_RtrOSPF):
    match = r"router-id (?P<id_>[.0-9]+)"

    def parse(self, cfg, id_):
        cfg["id"] = id_


class Cmd_RtrOSPF_AreaNSSA(CmdContext_RtrOSPF):
    match = (r"area (?P<area>\S[.0-9]+)"
             r" nssa(?P<no_redist> no-redistribution)?"
             r"(?P<no_summ> no-summary)?")

    def parse(self, cfg, area, no_redist, no_summ):
        n = deepsetdefault(cfg, "area", area, "nssa", last=set())
        if no_redist:
            n.add("no-redistribution")
        if no_summ:
            n.add("no-summary")


class Cmd_RtrOSPF_PasvInt(CmdContext_RtrOSPF):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        _ospf_passive_interface(cfg, int_name, not no)



# =============================================================================
# router ospfv3 ...
# =============================================================================



class Cmd_RtrOSPFv3(IndentedContextualCommand):
    match = r"router ospfv3 (?P<proc>\d+)"
    enter_context = "router-ospfv3"

    def parse(self, cfg, proc):
        return deepsetdefault(cfg, "router", "ospfv3", int(proc))


class CmdContext_RtrOSPFv3(IndentedContextualCommand):
    context = "router-ospfv3"


class Cmd_RtrOSPFv3_Id(CmdContext_RtrOSPFv3):
    match = r"router-id (?P<id_>[.0-9]+)"

    def parse(self, cfg, id_):
        cfg["id"] = id_


class Cmd_RtrOSPFv3_AreaNSSA(CmdContext_RtrOSPFv3):
    match = (r"area (?P<area>\S[.0-9]+)"
             r" nssa(?P<no_redist> no-redistribution)?"
             r"(?P<no_summ> no-summary)?")

    def parse(self, cfg, area, no_redist, no_summ):
        n = deepsetdefault(cfg, "area", area, "nssa", last=set())
        if no_redist:
            n.add("no-redistribution")
        if no_summ:
            n.add("no-summary")


class Cmd_RtrOSPFv3_AF(CmdContext_RtrOSPFv3):
    # "unicast" on the end is effectively ignored
    match = r"address-family (?P<af>ipv4|ipv6)( unicast)?"
    enter_context = "router-ospfv3-af"

    def parse(self, cfg, af):
        return deepsetdefault(cfg, "address-family", af)


class CmdContext_RtrOSPFv3_AF(CmdContext_RtrOSPFv3):
    context = "router-ospfv3-af"


class Cmd_RtrOSPFv3_AF_PasvInt(CmdContext_RtrOSPFv3_AF):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        _ospf_passive_interface(cfg, int_name, not no)


class Cmd_RtrOSPFv3_PasvInt(CmdContext_RtrOSPFv3):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        # the handling of this command outside of an address-family
        # block is a bit odd - it isn't stored at the router process
        # level but in the address family block and only affects the
        # currently defined address families, so if an address family
        # is added later, this will not propagate down
        for af in cfg.get("address-family", []):
            _ospf_passive_interface(
                cfg["address-family"][af], int_name, not no)
