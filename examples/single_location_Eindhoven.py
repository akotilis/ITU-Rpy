# -*- coding: utf-8 -*-
"""
In this code we calculate the athomsperhic channel for a optical (1550nm) link located in eindhoven, the netherlands.
"""

import itur
import matplotlib.pyplot as plt
import numpy as np

# # Location of eindhoven
lat = 51.26
lon = 5.28

# # Location of donetsk
# lat = 48.0
# lon = 37.48

# Link parameters
link_length = 5* itur.u.km  # Link length of 50 km
beam_divergence = 0.02479 * itur.u.mrad  # for both sides
capture_surface_diameter_m = 0.065 * itur.u.m  # Receiver aperture diameter of 0.065 m
dsd_shape_param = 0  # DSD shape parameter (0 for typical)

el = 60                # Elevation angle equal to 60 degrees
f = 22.5 * itur.u.GHz  # Frequency equal to 22.5 GHz
D = 1 * itur.u.m       # Receiver antenna diameter of 1 m
p_values = [10, 5, 1, 0.1, 0.01]                # We compute values exceeded during 0.1 % of the average
                       # year

# collect attenuation values for plotting
A_r_list = []
A_geo_list = []
A_w_list = []

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

    # store numeric attenuation (dB) for plotting
    try:
        A_r_db = A_r.to(itur.u.dB).value
    except Exception:
        try:
            A_r_db = float(A_r)
        except Exception:
            A_r_db = getattr(A_r, 'value', A_r)
    A_r_list.append(A_r_db)
    # store geometry and atmospheric components too
    try:
        A_geo_db = A_geo.to(itur.u.dB).value
    except Exception:
        A_geo_db = float(A_geo)
    A_geo_list.append(A_geo_db)
    try:
        A_w_db = A_w.to(itur.u.dB).value
    except Exception:
        try:
            A_w_db = float(A_w)
        except Exception:
            A_w_db = getattr(A_w, 'value', 0.0)
    A_w_list.append(A_w_db)


# Plot Rain attenuation vs exceedance probability (log-scale p)
try:
    plt.figure()
    plt.semilogx(p_values, A_r_list, marker='o')
    plt.gca().invert_xaxis()
    plt.xlabel('Exceedance probability (%)', fontsize=18)
    plt.ylabel('Rain attenuation (dB)', fontsize=18)
    plt.title('Rain attenuation vs exceedance probability (log-scale p)', fontsize=20)
    plt.grid(True, which='both', ls='--', lw=1)
    plt.show()
except Exception as e:
    print('Plotting failed:', e)

# --- Additional requested results ---
# 1) Rain attenuation as a function of availability
availability = [100.0 - p for p in p_values]
try:
    plt.figure()
    plt.plot(availability, A_r_list, marker='o')
    plt.xlabel('Availability (%)', fontsize=18)
    plt.ylabel('Rain attenuation (dB)', fontsize=18)
    plt.title('Rain attenuation vs availability', fontsize=20)
    plt.grid(True, ls='--', lw=1)
    plt.gca().invert_xaxis()
    plt.show()
except Exception as e:
    print('Availability plot failed:', e)

# 2) Sensitivity to optical geometry
try:
    diameters_m = np.linspace(0.02, 0.2, 10)  # receiver aperture diameters to test
    divergences_mrad = np.linspace(0.005, 0.05, 10)  # beam divergences to test

    Ageo_vs_d = []
    for d in diameters_m:
        A_geo_val = itur.models.itu1814.calculate_geometrical_attenuation(d * itur.u.m, link_length, beam_divergence)
        try:
            Ageo_vs_d.append(A_geo_val.to(itur.u.dB).value)
        except Exception:
            Ageo_vs_d.append(float(A_geo_val))

    Ageo_vs_b = []
    for b in divergences_mrad:
        A_geo_val = itur.models.itu1814.calculate_geometrical_attenuation(capture_surface_diameter_m, link_length, b * itur.u.mrad)
        try:
            Ageo_vs_b.append(A_geo_val.to(itur.u.dB).value)
        except Exception:
            Ageo_vs_b.append(float(A_geo_val))

    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(diameters_m, Ageo_vs_d, marker='o')
    plt.xlabel('Receiver aperture diameter (m)')
    plt.ylabel('Geometrical attenuation (dB)')
    plt.title('Geometry sensitivity: aperture')
    plt.grid(True, ls='--', lw=1)

    plt.subplot(1,2,2)
    plt.plot(divergences_mrad, Ageo_vs_b, marker='o')
    plt.xlabel('Beam divergence (mrad)')
    plt.ylabel('Geometrical attenuation (dB)')
    plt.title('Geometry sensitivity: divergence')
    plt.grid(True, ls='--', lw=1)
    plt.tight_layout()
    plt.show()
except Exception as e:
    print('Geometry sensitivity plot failed:', e)

# 3) Total attenuation and outage
system_losses_db = 2.0  # example system losses (dB)
link_margin_db = 24.0    # example link margin (dB)
total_att_list = []
for ar, ag, aw in zip(A_r_list, A_geo_list, A_w_list):
    total = ar + ag + aw + system_losses_db
    total_att_list.append(total)

try:
    plt.figure()
    plt.plot(availability, total_att_list, marker='o', label='Total attenuation')
    plt.axhline(link_margin_db, color='r', linestyle='--', label=f'Link margin = {link_margin_db} dB')
    plt.xlabel('Availability (%)')
    plt.ylabel('Total attenuation (dB)')
    plt.title('Total attenuation vs availability (outage when > link margin)')
    plt.grid(True, ls='--', lw=1)
    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()
except Exception as e:
    print('Total attenuation plot failed:', e)

# Print outage summary
for p, avail, total in zip(p_values, availability, total_att_list):
    outage = total > link_margin_db
    print(f"p={p}% avail={avail}% total_att={total:.2f} dB outage={outage}")
