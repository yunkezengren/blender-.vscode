def link_points(link, v2d, curv):
    fs, ts = link.from_socket, link.to_socket
    try:
        if not (fs.enabled and ts.enabled):
            return None
        sf = BNodeSocket.from_address(fs.as_pointer())
        st = BNodeSocket.from_address(ts.as_pointer())
        if not (sf.runtime and st.runtime):
            return None
        rf, rt = sf.runtime.contents, st.runtime.contents
        x1, y1 = rf.location[0], rf.location[1]
        x2, y2 = rt.location[0], rt.location[1]
    except:
        return None
    dx, dy = x2 - x1, y2 - y1
    h = (dx if dx >= 0 else math.hypot(dx, dy)) * curv
    p0, p1, p2, p3 = (x1, y1), (x1 + h, y1), (x2 - h, y2), (x2, y2)
    v2r = v2d.view_to_region
    r0, r3 = v2r(*p0, clip=False), v2r(*p3, clip=False)
    approx = abs(r3[0] - r0[0]) + abs(r3[1] - r0[1])
    seg = max(SEG_MIN, min(SEG_MAX, int(approx * 0.055)))
    coeff, pts = _BEZIER_TABLE[seg], [None] * (seg + 1)
    for i, (a, b, c, d) in enumerate(coeff):
        x = a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0]
        y = a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]
        pts[i] = v2r(x, y, clip=False)
    return pts
