# Directions Key

The GTFS data, vehicle tracking and predictions data all contain "direction" fields for each entry. This document shows how each direction field value maps between these data sources.

801:
    raw json: 0/180
    schedule: 0 (7th St Metro - north) / 1 (dt Long beach - south)
    prediction json:
        predictions array: 0
        headsign: 7th St Metro
        dirTag: 801_0_var1
        //
        predictions array: 1
        headsign: Downtown Long Beach
        dirTag: 801_1_var1

802:
    raw json: 90/270
    schedule: 0 (union - east) / 1 (north hollywood - west)
    prediction json:
        predictions array: 0
        headsign: Union Station
        dirTag: 802_0_var0
        //
        predictions array: 1
        headsign: North Hollywood
        dirTag: 802_1_var0

803:
    raw json: 90/270
    schedule: 0 (norwalk - east) / 1 (redondo - west)
    prediction json:
        predictions array: 0
        headsign: redondo
        dirTag: 803_1_var0
        //
        predictions array: 1
        headsign: norwalk
        dirTag: 803_0_var0

804:
    raw json: 0/180
    schedule: 0 (azusa - north) / 1 (atlantic - south)
    prediction json:
        predictions array: 0
        headsign: atlantic
        dirTag: 804_1_var0
        //
        predictions array: 1
        headsign: azusa
        dirTag: 804_0_var0
    
805:
    raw json: 90/270
    schedule: 0 (union - east) / 1 (wilshire western - west)
    predictions json:
        headsign: wilshire western
        dirTag: 805_1_var0
        //
        headsign: union
        dirTag: 805_0_var0

806:
    raw json: 0/180
    schedule: 0 (7th st - east) / 1 (santa monica - west)
    prediction json:
        headsign: santa monica
        dirTag: 806_1_var0
        //
        headsign: 7th st
        dirTag: 806_0_var0
    