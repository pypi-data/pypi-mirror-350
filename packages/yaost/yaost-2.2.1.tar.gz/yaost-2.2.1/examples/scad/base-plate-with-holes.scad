$fa=3.000000;
$fs=0.500000;
difference(){cube([60,60,3]);union(){union(){translate([8,8,0])translate([0,0,-5000])cylinder(d=10,h=10000);translate([30,0,0])mirror([1,0,0])translate([-30,0,0])translate([8,8,0])translate([0,0,-5000])cylinder(d=10,h=10000);}translate([0,30,0])mirror([0,1,0])translate([0,-30,0])union(){translate([8,8,0])translate([0,0,-5000])cylinder(d=10,h=10000);translate([30,0,0])mirror([1,0,0])translate([-30,0,0])translate([8,8,0])translate([0,0,-5000])cylinder(d=10,h=10000);}}}
