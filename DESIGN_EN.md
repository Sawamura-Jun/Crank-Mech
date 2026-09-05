# Metalworking Specifications and Assembly Procedure

This document covers the standard design with a crank radius of 30 mm and a connecting rod center-to-center distance of 120 mm. All dimensions are in mm. The mechanism is intended as a hand-operated, unloaded teaching aid for observing rotary and reciprocating motion. No ratings have been established for motor-driven operation or load transmission.

## Main Specifications

| Item | Design Value |
|---|---:|
| Base | 250 × 120 × 14, outer corner radius R5 |
| Crank disk | Outside diameter 86, thickness 10, crank radius 30 |
| Connecting rod | Center-to-center distance 120, overall length 140, width 20, thickness 6 |
| Stroke | 60 |
| Slider center position | X=90–150 from the main shaft centerline |
| Effective guide length | X=65–175, length 110 |
| Highest point | Z=84.95 (top of the hand grip retaining screw) |
| Custom-made parts | 14 types, 20 pieces |
| Purchased parts | Hexagon socket head cap screws: 5 types, 13 pieces |

X is the direction of slider travel, Y is the base width direction, and Z is upward. The assembly origin is on the underside of the base, directly below the fixed main shaft centerline. The base occupies X=-55–195, Y=-60–60, Z=0–14. Distinguish between the coordinates in the individual-part STEP files and the assembly coordinates.

## Materials and General Machining Instructions

The base, guides, end stops, crank, and connecting rod are specified as A6061-T6; the slider, bushings, and hand grip as machinable brass; and the stepped shafts as S45C. The retaining washers are custom-made steel parts. The parts can be manufactured by turning, milling, drilling, and tapping.

Unless otherwise specified, dimensional tolerances are ±0.10 and hole position tolerances are ±0.05. Target a flatness of 0.05 or better on the top surface of the base and parallelism between the two guides within 0.05 over a length of 110. Target a surface finish of Ra1.6 or better on sliding surfaces and Ra0.8 or better on rotating shafts and bushing bores. Target bearing coaxiality and shaft shoulder and end-face perpendicularity within 0.02.

Remove all burrs and chamfer unspecified sharp external edges to C0.2–0.5. Do not alter the sliding datum surfaces, effective press-fit lengths, or shoulder heights when deburring or chamfering. Where an internal corner retains a tool radius, check for interference with the mating part's relief or chamfer. The individual dimensional tolerances specified below take precedence.

## Custom-Made Part Dimensions

| ID | Individual-Part STEP Datums and Main Machining Dimensions |
|---|---|
| P01 | Base. M6×1 through-tapped hole for the fixed shaft at (0,0). Mounting holes: 4-Ø6.6 at (-45,±50) and (185,±50). Guide mounting holes: 6-M5×0.8 through-tapped at X=80/120/160, Y=±22.1. End stop mounting holes: 4-M5×0.8 through-tapped at X=59/181, Y=±22. |
| P02 | 2 identical parts. X=-55–55, Y=0–17, Z=0–25.3. Remove the corner region Y=0–5, Z=0–20.30 to form an L-shaped cross-section. 3-Ø5.5 through-holes at (X,Y)=(-40,12)/(0,12)/(40,12). Counterbore Ø9 to a depth of 5.5 from the top surface. |
| P03 | 2 identical parts. 12 × 56 × 8, centered on the XY origin, with the bottom surface at Z=0. 2-Ø5.5 holes at (0,±22). Counterbore Ø9 to a depth of 5.5 from the top surface. Outer corner radius R1. |
| P04 | Ø86 × 10. Central Ø16 press-fit bore for the bushing. M5×0.8 through-tapped hole at (30,0) and Ø18 lightening hole at (-24,0). C0.5 chamfers on the upper and lower outside edges. |
| P05 | Semicircular ends R10, center-to-center distance 120, thickness 6. Bushing bores: 2-Ø12 at (0,0) and (120,0). |
| P06 | Brass slider. X=-16–16. Width 30 from the bottom surface to a height of 20; width 20 over the next 4.35. Overall height 24.35. Central M5×0.8 through-tapped hole. C0.5 chamfers on vertical edges. |
| P07 | Fixed main shaft. Lower flange Ø22 × 14.20, upper shaft Ø12 × 10.30, overall length 24.50. Central Ø6.6 through-hole. |
| P08 | 2 identical parts. Lower flange Ø16 × 9.00, upper shaft Ø8 × 6.30, overall length 15.30. Central Ø5.5 through-hole. |
| P09 | Hand grip shaft. Lower flange Ø12 × 1.00, upper shaft Ø8 × 23.30, overall length 24.30. Central Ø5.5 through-hole. |
| P10 | Main shaft bushing. Nominal outside diameter 16, finished bore diameter 12.04, length 10. Outside diameter shall follow the press-fit tolerances below. |
| P11 | 2 identical parts. Connecting rod bushing. Nominal outside diameter 12, finished bore diameter 8.04, length 6. Outside diameter shall follow the press-fit tolerances below. |
| P12 | Revolving hand grip. Outside diameter 20, finished bore diameter 8.04, length 23. C0.5 chamfers on the inner and outer edges at both ends. |
| P13 | Custom retaining washer. Outside diameter 18, inside diameter 6.6, thickness 1.60. |
| P14 | 3 identical parts. Custom retaining washer. Outside diameter 15, inside diameter 5.5, thickness 1.00. |

## Fits and Sliding Clearances

The STEP files do not contain embedded tolerance symbols or PMI. The table below specifies the required machining dimensions for this design. Machining both mating press-fit features to the nominal diameters in the STEP files will not provide retention; the dimensions below must be applied.

| Location | Actual Hole Diameter Range | Actual Shaft or Bushing Outside Diameter Range | Result |
|---|---:|---:|---|
| Crank and P10 bushing | 16.000–16.010 | 16.020–16.030 | Diametral interference 0.010–0.030 |
| Connecting rod and P11 bushing | 12.000–12.010 | 12.020–12.030 | Diametral interference 0.010–0.030 |
| P10 bore and P07 shaft | 12.030–12.050 | 11.980–12.000 | Diametral clearance 0.030–0.070 |
| P11 bore and P08 shaft | 8.030–8.050 | 7.980–8.000 | Diametral clearance 0.030–0.070 |
| Hand grip bore and P09 shaft | 8.030–8.050 | 7.980–8.000 | Diametral clearance 0.030–0.070 |

Finish the bushing bores to their final dimensions after press-fitting. Provide a small lead-in chamfer at the entry and support the parent part during pressing. Keep each bushing end face flush with the corresponding mating-part end face within ±0.02, avoiding axial protrusion.

The crank thickness of 10, connecting rod thickness of 6, hand grip length of 23, and corresponding effective shaft lengths of 10.30/6.30/23.30 have a tolerance of ±0.02. Custom retaining washer thickness has a tolerance of ±0.02, and shaft flange height has a tolerance of ±0.03. Each rotating assembly has a nominal total axial endplay of 0.30, allowing the part to rotate even with the screw tightened.

The slider widths of 30/20 have a tolerance of +0/-0.02, and the lower section height of 20 has a tolerance of ±0.02. The guide recess height of 20.30 has a tolerance of ±0.02. After assembly, adjust the inside guide width to 30.20 and the upper opening to 20.20, each within ±0.03. The nominal total lateral clearance is 0.20, and the nominal total vertical clearance is 0.30. The bottom of the slider travels in contact with the lubricated top surface of the base.

## Thread Machining and Purchased Parts

**In the STEP files, internal threads are simplified as holes at the nominal thread diameter, and external threads as cylinders at the nominal thread diameter. Do not use the STEP hole diameters directly for machining tapped holes.**

- M5×0.8: drill Ø4.2 and tap through.
- M6×1.0: drill Ø5.0 and tap through.
- Helical thread geometry is omitted. The heads of purchased screws are reference geometry for placement verification only.
- Screw length is measured from under the head and excludes the head. Select hexagon socket head cap screws with M5 heads no larger than Ø8.5 × height 5 and M6 heads no larger than Ø10 × height 6.

| Screw | Quantity | Location | Design Thread Engagement |
|---|---:|---|---:|
| M6×40 | 1 | Main shaft retention | 13.90 |
| M5×30 | 6 | Guide retention | 10.20 |
| M5×12 | 4 | End stop retention | 9.50 |
| M5×25 | 1 | Connecting rod shaft on the slider side | 8.70 |
| M5×50 | 1 | Shared retention of the crank-side shaft and hand grip | 8.40 |

The tip of the main shaft retaining screw is nominally recessed 0.10 from the underside of the base. Check the actual screw length and washer thickness to ensure that the tip does not protrude below the base. If it protrudes, machine the tip as required. If commercially available standard washers are substituted for the custom retaining washers P13/P14, recheck the clearances and thread engagement affected by differences in thickness and diameter.

## Assembly Positions and Procedure

| Surface or Part | Z Position in the Assembly |
|---|---:|
| Base top surface / slider bottom surface | 14.00 |
| Main shaft shoulder | 28.20 |
| Crank bottom to top surfaces | 28.35–38.35 (shown at the midpoint of the axial endplay) |
| Slider top surface | 38.35 |
| Guide top surface | 39.30 |
| Top of the main shaft retaining screw | 46.10 |
| Connecting rod bottom to top surfaces | 47.50–53.50 |
| Hand grip bottom to top surfaces | 55.80–78.80 |

1. Deburr all parts and check the tapped holes, counterbores, and fit dimensions. Press-fit the bushings into the crank and connecting rod, then finish the bores.
2. Place the slider on the base. Position one P02 guide at (X,Y)=(120,10.1). Rotate the opposite guide 180° about the Z-axis and position it at (120,-10.1). Loosely secure the guides with 6 M5×30 screws.
3. Use feeler gauges to adjust the clearances on both sides and the guide parallelism so that the slider travels freely over the full length, then tighten the screws. Install the P03 end stops at X=59 and 181 using 2 M5×12 screws for each stop.
4. Position the P07 main shaft at the base origin, fit the crank over it, and secure it with the P13 custom retaining washer and an M6×40 screw. Confirm that the washer seats against the shaft end and that the disk rotates freely.
5. Place 1 P08 shaft over each of the crank and slider holes, and fit the connecting rod with its bushings over the shafts. Secure the slider side with a P14 washer and an M5×25 screw.
6. On the crank side, stack the parts in this order: P14 washer → P09 hand grip shaft → P12 hand grip → P14 washer. Secure the stack to the crank with an M5×50 screw. Confirm that the hand grip and connecting rod rotate independently.
7. Apply a small amount of machine oil to the sliding surfaces and each shaft, then slowly turn the mechanism through one full revolution. Check operation at the inner and outer dead centers, screw loosening, axial endplay, and any binding in the guides. Use a removable thread-locking compound on the retaining screws if necessary.
8. For classroom use, secure the base to a supporting platform using the Ø6.6 mounting holes and operate the mechanism by holding the hand grip. The areas around the linkage and slider present finger pinch points; do not touch these areas while the mechanism is moving.

Bolts and nuts for securing the mechanism to a supporting platform are not included in the bill of materials, as they must be selected to suit the platform thickness.

## Scope of Verification

Each of the 19 distinct part geometries is checked to ensure that it consists of a single valid solid. Volume and overall dimensions are checked by reimporting the STEP files. The assembly STEP file contains 33 solids. Center-to-center distances, the 60 mm stroke, and the guide travel limits are checked at 1° increments. Interference is checked using solid intersection volumes at 24 positions in 15° increments. The evaluation threshold is 1e-5 mm³.

In the nominal model, the clearance between the underside of the connecting rod and the main shaft retaining screw head is 1.40. The minimum margin between the slider end and the guide end is 9.00. Press fits are verified using nominal surface contact, and threads are verified using simplified geometry. Checking 24 positions does not provide a mathematical guarantee for every angle throughout continuous motion. Machining errors, elastic deformation, friction, wear, and durability require verification on the physical mechanism.
