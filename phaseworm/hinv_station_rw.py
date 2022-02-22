"""
HypoInverse station data file reading and writing.

:copyright:
    2020-2021   Jean-Marie Saurel <saurel@ipgp.fr>
                Lise Retailleau <retailleau@ipgp.fr>
                Claudio Satriano <satriano@ipgp.fr>

:license:
    GNU General Public License 3.0
    https://www.gnu.org/licenses/gpl-3.0.en.html
"""


def read_fortran_str(deb_len, line):
    """Read string : len characters from deb in line."""
    deb = deb_len[0] - 1
    length = deb_len[1]
    try:
        s = line[deb:deb + length].strip()
    except Exception:
        s = ''
    return(s)


def read_fortran_float(deb_len, line):
    """Read float : len characters from deb in line."""
    deb = deb_len[0] - 1
    length = deb_len[1]
    try:
        f = float(line[deb:deb + length].strip())
    except Exception:
        f = 0.0
    return(f)


def read_fortran_int(deb_len, line):
    """Read float : len characters from deb in line."""
    deb = deb_len[0] - 1
    length = deb_len[1]
    try:
        i = int(line[deb:deb + length].strip())
    except Exception:
        i = 0
    return(i)


def read_hinv(hfile):
    """Read Hypo2000 station file and returns inventory."""
    from obspy.core.inventory import Network
    from obspy.core.inventory import Station
    from obspy.core.inventory import Channel
    from obspy.core.inventory import Inventory
    try:
        f = open(hfile, 'r')
    except Exception:
        inv = Inventory()
    inv = Inventory()
    for line in f.readlines():
        sta = read_fortran_str((1, 5), line)
        net = read_fortran_str((7, 2), line)
        chan = read_fortran_str((11, 3), line)
        loccode = read_fortran_str((81, 2), line)
        latd = read_fortran_int((16, 2), line)
        latm = read_fortran_float((19, 7), line)
        latsign = read_fortran_str((26, 1), line)
        if 'S' in latsign:
            lat = - (latd + latm/60)
        else:
            lat = latd + latm/60
        lond = read_fortran_int((27, 3), line)
        lonm = read_fortran_float((31, 7), line)
        lonsign = read_fortran_str((38, 1), line)
        if 'E' in lonsign:
            lon = lond + lonm/60
        else:
            lon = - (lond + lonm/60)
        elev = read_fortran_float((39, 4), line)
        depth = 0
        new_net = Network(code=net)
        new_sta = Station(code=sta,
                          latitude=lat,
                          longitude=lon,
                          elevation=elev)
        new_net.stations.append(new_sta)
        new_chan = Channel(code=chan,
                           location_code=loccode,
                           latitude=lat,
                           longitude=lon,
                           elevation=elev,
                           depth=depth)
        new_sta.channels.append(new_chan)
        n = inv.select(network=net)
        s = inv.select(network=net, station=sta)
        c = inv.select(network=net, station=sta, channel=chan)
        if not len(n):
            # Network doesn't exist
            inv.networks.append(new_net)
        elif not len(s):
            # Network exist, station doesn't exist
            for (i, n) in enumerate(inv.networks):
                if n.code == net:
                    break
            inv.networks[i].stations.append(new_sta)
        elif not len(c):
            # Network and station exist, channel doesn't exist
            for (i, n) in enumerate(inv.networks):
                if n.code == net:
                    for (j, s) in enumerate(inv.networks[i].stations):
                        if s.code == sta:
                            break
            inv.networks[i].stations[j].channels.append(new_chan)
    f.close()
    return inv


def inv2hline(net, sta, loc_cha):
    """Print Hypo2000 station line from ObsPy inventory objects."""
    chan = loc_cha.code
    loc = loc_cha.location_code
    lat = abs(loc_cha.latitude)
    ilat = int(lat)
    dlat = (lat - ilat) * 60
    hlat = 'N' if loc_cha.latitude > 0 else 'S'
    lon = abs(loc_cha.longitude)
    ilon = int(lon)
    dlon = (lon - ilon) * 60
    hlon = 'E' if loc_cha.longitude > 0 else 'W'
    elev = loc_cha.elevation
    hline = str('%-5s %-2s  %3s  %2d %7.4f%1c%3d %7.4f%1c%4d'
                % (sta.code, net.code, chan,
                   ilat, dlat, hlat,
                   ilon, dlon, hlon, elev))
    hline = hline + str('%3.1f    %5.2f %5.2f %5.2f %5.2f  %6.2f'
                        % (0, 0, 0, 0, 0, 0))
    hline = hline + str('%2s\n' % (loc))
    return hline


def print_hinv(inv):
    """Print Hypo2000 station file from ObsPy inventory."""
    n = 0
    for net in inv:
        for sta in net:
            for loc_cha in sta:
                hline = inv2hline(net, sta, loc_cha)
                print(hline)
                n = n + 1
    return n


def write_hinv(inv, hfile):
    """Write Hypo2000 station file from ObsPy inventory."""
    n = 0
    try:
        f = open(hfile, 'w')
    except Exception:
        return n
    for net in inv:
        for sta in net:
            for loc_cha in sta:
                hline = inv2hline(net, sta, loc_cha)
                f.write(hline)
                n = n + 1
    f.close()
    return n
