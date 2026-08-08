from chronovore.helpers.get import *

from flask import *

from chronovore.__main__ import app

@app.get("/faction/<faction>")
def faction_faction(faction):

    f = get_faction(faction)

    return render_template("faction.html", f=f)


@app.get("/faction/<faction>/detachment/<detachment>")
def faction_faction_detachment_detachment(faction, detachment):

    f = get_faction(faction)

    d = f.detachment(detachment)

    return render_template("detachment.html", f=f, d=d)

@app.get("/faction/<faction>/unit/<unit>")
@app.get("/faction/<faction>/detachment/<detachment>/unit/<unit>")
def faction_faction_unit_unit(faction, unit, detachment=None):

    f=get_faction(faction)
    color=f.color

    u = f.unit(unit)

    if detachment:
        d=f.detachment(detachment)
        if not d.is_legal(u):
            abort(404)
        color=d.color
    else:
        d=None

    return render_template(
        "unit.html", 
        f=f, 
        u=u, 
        d=d, 
        color=color)

@app.get("/faction/<faction>/detachment/<detachment>/armylist")
def faction_faction_detachment_detachment_armylist(faction, detachment):

    f=get_faction(faction)
    color=f.color

    d=f.detachment(detachment)

    units = []

    for role in f.unit_listing:
        for unit in f.unit_listing[role]:
            if session.get(f'qty_{f.id}_{unit.id}', 0) and d.is_legal(unit):
                units.append(unit)

    units.sort(key=lambda x:x.name)

    return render_template(
        "army.html",
        f=f,
        d=d,
        color=color,
        units=units
        )
