"""
Canned network troubleshooting scenarios used as a fallback when the
Anthropic API is unavailable (no key set, rate-limited, or offline).
Also useful for generating README screenshots without live API calls.
"""
#I am a certified Forti OS administrator and Sangfor  XDR and HCI Cerified 

DEMO_SCENARIOS = [
    {#these are the kewords in the app.py
        "keywords": ["ospf", "exstart", "neighbor stuck"],
        "topic": "OSPF Neighbor Stuck in EXSTART",
        "response": (
            "An OSPF neighbor stuck in EXSTART almost always points to an MTU "  #this is the first case
            "mismatch between the two routers, since EXSTART is where they "
            "negotiate Database Description (DBD) packet size.\n\n"
            "1. Check the interface MTU on both sides: `show interface <int>` "
            "and confirm they match.\n"
            "2. If MTU matches, check for `ip ospf mtu-ignore` on one side but "
            "not the other — this needs to be consistent.\n"
            "3. Rule out a duplex/speed mismatch causing packet corruption.\n"
            "4. Confirm there's no ACL silently dropping OSPF (protocol 89) "
            "between the two routers.\n\n"
            "If MTU and ACLs check out, capture packets on both ends during "
            "the negotiation to see exactly where the DBD exchange stalls."
        ),
    },
    {
        "keywords": ["fortigate", "ha", "high availability", "not forming"],#Fortigate is also in the help list
        "topic": "FortiGate HA Not Forming",
        "response": (
            "FortiGate HA pairs fail to form for a handful of common reasons. "
            "Work through these in order:\n\n"
            "1. Confirm both units are running the identical firmware version "
            "— HA will refuse to form on mismatched builds.\n"
            "2. Check the HA mode (Active-Passive vs Active-Active) matches "
            "on both units.\n"
            "3. Verify the HA group-id and password are identical.\n"
            "4. Confirm the heartbeat interfaces are cabled correctly and not "
            "accidentally swapped with a data interface.\n"
            "5. Check `diagnose sys ha status` for split-brain or version "
            "mismatch errors.\n\n"
            "A frequent gotcha: heartbeat interfaces need to be on isolated "
            "links, not routed through a switch with STP delays — that alone "
            "can prevent HA negotiation from completing in time."
        ),
    },
    {
        "keywords": ["vpn", "ipsec", "phase 1", "phase 2", "tunnel down"],
        "topic": "IPsec VPN Tunnel Won't Establish",
        "response": (
            "Break this into Phase 1 and Phase 2 separately rather than "
            "treating it as one problem:\n\n"
            "Phase 1 (ISAKMP/IKE): confirm pre-shared keys match exactly, "
            "encryption/hash/DH group proposals match on both peers, and "
            "that UDP 500 (and 4500 if NAT-T is involved) isn't blocked.\n\n"
            "Phase 2 (IPsec SA): confirm the proxy-IDs / interesting traffic "
            "(the subnets defined in the crypto ACL or selectors) match "
            "exactly on both ends — even a /24 vs /23 mismatch will fail "
            "silently.\n\n"
            "Check logs for the specific failure stage: if Phase 1 completes "
            "but Phase 2 doesn't, it's almost always a selector mismatch."
        ),
    },
    {
        "keywords": ["dns", "resolve", "nslookup", "name resolution"],
        "topic": "DNS Resolution Failures",
        "response": (
            "Start by isolating whether this is a resolution problem or a "
            "reachability problem:\n\n"
            "1. Run `nslookup <domain> <dns-server-ip>` directly against the "
            "DNS server to bypass local cache/resolver issues.\n"
            "2. If that fails, test reachability to the DNS server itself "
            "with `ping` and `telnet <dns-ip> 53`.\n"
            "3. If resolution works against an external DNS (e.g. 8.8.8.8) "
            "but not the internal one, the problem is your internal DNS "
            "server or its forwarders.\n"
            "4. Check for split-DNS or conditional forwarding misconfig if "
            "internal names resolve but external ones don't, or vice versa."
        ),
    },
    {
        "keywords": ["nat", "port forward", "translation"],
        "topic": "NAT / Port Forwarding Not Working",
        "response": (
            "Work through this in layers:\n\n"
            "1. Confirm the NAT rule itself is correctly bound to the right "
            "interface (inbound on WAN, not LAN).\n"
            "2. Check that a corresponding firewall policy allows the "
            "translated traffic — NAT and the security policy are usually "
            "separate rule sets and both need to be correct.\n"
            "3. Verify the internal host's default gateway points back "
            "through the firewall, not a different path, or return traffic "
            "won't follow the same NAT'd path.\n"
            "4. Use `telnet <public-ip> <port>` from outside the network to "
            "isolate whether the issue is NAT, the firewall policy, or the "
            "internal service itself not listening."
        ),
    },
    {
        "keywords": ["ad", "active directory", "domain controller", "replication"],
        "topic": "Active Directory Replication Issues",
        "response": (
            "AD replication problems usually trace back to one of these:\n\n"
            "1. Run `repadmin /replsummary` to get a quick view of which DCs "
            "are failing and the error codes involved.\n"
            "2. Check DNS first — AD relies heavily on SRV records, and a "
            "broken DNS entry will break replication before anything else "
            "is even worth checking.\n"
            "3. Verify time sync (`w32tm /query /status`) — replication "
            "fails if DCs drift more than 5 minutes apart by default.\n"
            "4. Check firewall rules between sites for the required AD "
            "ports (135, 389, 445, 3268, and the RPC dynamic port range)."
        ),
    },
]


def find_demo_response(user_message: str) -> str | None:
    """
    Match a user message against demo scenario keywords.
    Returns the canned response text, or None if no match is found
    (caller should show a generic fallback in that case).
    """
    if not user_message:
        return None

    message_lower = user_message.lower()
    for scenario in DEMO_SCENARIOS:
        if any(keyword in message_lower for keyword in scenario["keywords"]):
            return scenario["response"]

    return None


GENERIC_FALLBACK = (
    "I'm currently running in demo mode (no live API connection), so I can "
    "only respond to a few pre-built scenarios: OSPF EXSTART issues, "
    "FortiGate HA problems, IPsec VPN tunnels, DNS resolution, NAT/port "
    "forwarding, and Active Directory replication. Try asking about one of "
    "those, or check the sidebar for quick topic buttons."
)
