# -*- coding: utf-8 -*-
"""
In this code we calculate the athomsperhic channel for a optical (1550nm) link located in eindhoven, the netherlands.
"""

import itur

# # Location of eindhoven
lat = 51.26
lon = 5.28

# # Location of donetsk
# lat = 48.0
# lon = 37.48

# Link parameters
link_length = 15* itur.u.km  # Link length of 50 km
beam_divergence = 0.02479 * itur.u.mrad  # for both sides
capture_surface_diameter_m = 0.065 * itur.u.m  # Receiver aperture diameter of 0.065 m
dsd_shape_param = 0  # DSD shape parameter (0 for typical)

el = 60                # Elevation angle equal to 60 degrees
f = 22.5 * itur.u.GHz  # Frequency equal to 22.5 GHz
D = 1 * itur.u.m       # Receiver antenna diameter of 1 m
p_values = [10, 5, 1, 0.1, 0.01]                # We compute values exceeded during 0.1 % of the average
                       # year
for p in p_values:
    print(f"\n\nCalculations for p={p}% of the average year:")
    # Compute atmospheric parameters
    hs = itur.topographic_altitude(lat, lon)
    T = itur.surface_mean_temperature(lat, lon)
    P = itur.models.itu835.pressure(lat, hs)
    rho_p = itur.surface_water_vapour_density(lat, lon, p, hs)
    rho_sa = itur.models.itu835.water_vapour_density(lat, hs)
    T_sa = itur.models.itu835.temperature(lat, hs)
    V = itur.models.itu836.total_water_vapour_content(lat, lon, p, hs)

    # print(
    #     f"The ITU recommendations predict the following values for the point located at coordinates ({lat}, {lon})"
    # )

    # print(
    #     f"  - Height above the sea level                  [ITU-R P.1511]  {hs.to(itur.u.m):.1f}"
    # )
    T_C = T.to(itur.u.Celsius, equivalencies=itur.u.temperature())
#     print(f"  - Surface mean temperature                    [ITU-R P.1510]  {T_C:.1f}")
#     print(f"  - Surface pressure                            [ITU-R P.835]   {P:.1f}")
#     T_sa_C = T_sa.to(itur.u.Celsius, equivalencies=itur.u.temperature())
#     print(f"  - Standard surface temperature                [ITU-R P.835]   {T_sa_C:.1f}")
#     print(f"  - Standard water vapour density               [ITU-R P.835]   {rho_sa:.1f}")
#     print(f"  - Water vapor density (p={p}%)                [ITU-R P.836]   {rho_p:.1f}")
#     print(f"  - Total water vapour content (p={p}%)         [ITU-R P.836]   {V:.1f}")

    # Compute rain and cloud-related parameters
    R_prob = itur.models.itu618.rain_attenuation_probability(lat, lon, el, hs)
    R_pct = itur.models.itu837.rainfall_probability(lat, lon)
    R001 = itur.models.itu837.rainfall_rate(lat, lon, p)
    h_0 = itur.models.itu839.isoterm_0(lat, lon)
    h_rain = itur.models.itu839.rain_height(lat, lon)
    L_red = itur.models.itu840.columnar_content_reduced_liquid(lat, lon, p)
    A_w = itur.models.itu676.zenit_water_vapour_attenuation(lat, lon, p, f, h=hs)

    #print(f"  - Rain attenuation probability                [ITU-R P.618]   {R_prob:.1f}")
    #print(f"  - Rain percentage probability                 [ITU-R P.837]   {R_pct:.1f}")
    #print(f"  - Rainfall rate exceeded for p={p}%           [ITU-R P.837]   {R001:.1f}")
    #print(f"  - Rain height                                 [ITU-R P.839]   {h_rain:.1f}")
    #print(f"  - Columnar content of reduced liquid (p={p}%) [ITU-R P.840]   {L_red:.1f}")
    #print(f"  - Zenit water vapour attenuation (p={p}%)     [ITU-R P.676]   {A_w:.1f}")

    #print(f"\n\nlink margin calculation the total link margin is: M_link = P_e - S_r - A_system - A_geo - A_atmo")
    # Compute attenuation values
    A_geo = itur.models.itu1814.calculate_geometrical_attenuation(capture_surface_diameter_m, link_length, beam_divergence)

    #print(f"  - Geometrical attenuation                     [ITU-R P.1814]   {A_geo:.1f}")

    A_r_specific = itur.models.itu1814.specific_attenuation_due_to_rain(R001, dsd_shape_param)
    A_r = itur.models.itu1814.path_attentuation_due_to_rain(R001, dsd_shape_param, link_length)


    print(
        f"\n\nAttenuation values exceeded for p={p}% of the average year "
        f"for a link with length={link_length} \nD={D} and "
        f"with location at coordinates ({lat}, {lon})"
    )

    print(f"  - specific Rain attenuation for p={p}% of the time[ITU-R P.1814]   {A_r_specific:.1f}")
    print(f"  - Rain attenuation for p={p}% of the timefor total link [ITU-R P.1814]   {A_r:.1f}")
