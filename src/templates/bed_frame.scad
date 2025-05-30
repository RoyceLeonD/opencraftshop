// Parametric bed frame design
include <lumber_lib.scad>

// Default parameters (Queen size: 60" x 80")
bed_length = 80;
bed_width = 60;
bed_height = 14;  // Standard bed frame height
headboard_height = 36;
mattress_support_slats = 13;  // Number of support slats

// Module for bed rails (sides)
module bed_rail(length) {
    lumber("2x10", length);
}

// Module for bed posts
module bed_post(height) {
    lumber("4x4", height);
}

// Module for support slats
module support_slat(width) {
    lumber("1x4", width);
}

// Module for center support beam
module center_support(length) {
    lumber("2x6", length);
}

// Module for headboard
module headboard(width, height) {
    // Vertical posts
    for (x = [0, width - lumber_width("2x4")]) {
        translate([x, 0, 0])
            lumber("2x4", height);
    }
    
    // Horizontal rails
    for (z = [0, height/2, height - lumber_thickness("2x6")]) {
        translate([0, 0, z])
            rotate([0, 90, 0])
            lumber("2x6", width);
    }
    
    // Vertical slats (1x4)
    slat_spacing = (width - lumber_width("2x4") * 2) / 5;
    for (i = [0:4]) {
        translate([lumber_width("2x4") + i * slat_spacing + i * lumber_width("1x4"), 
                   lumber_thickness("2x4"), 
                   lumber_thickness("2x6")])
            lumber("1x4", height - 2 * lumber_thickness("2x6"));
    }
}

// Main bed frame assembly
module bed_frame(length, width, height, headboard_h, num_slats) {
    rail_height = lumber_width("2x10");
    
    // Corner posts
    post_positions = [
        [0, 0, 0],
        [length - lumber_width("4x4"), 0, 0],
        [0, width - lumber_width("4x4"), 0],
        [length - lumber_width("4x4"), width - lumber_width("4x4"), 0]
    ];
    
    // Regular posts (without headboard)
    for (i = [2:3]) {
        translate(post_positions[i])
            bed_post(height + rail_height);
    }
    
    // Headboard posts (taller)
    for (i = [0:1]) {
        translate(post_positions[i])
            bed_post(headboard_h);
    }
    
    // Side rails (2x10)
    translate([lumber_width("4x4"), 0, height])
        rotate([90, 0, 0])
        rotate([0, 90, 0])
        bed_rail(length - 2 * lumber_width("4x4"));
    
    translate([lumber_width("4x4"), width, height])
        rotate([90, 0, 0])
        rotate([0, 90, 0])
        bed_rail(length - 2 * lumber_width("4x4"));
    
    // Head and foot rails
    translate([0, lumber_width("4x4"), height])
        rotate([90, 0, 90])
        rotate([0, 90, 0])
        bed_rail(width - 2 * lumber_width("4x4"));
    
    translate([length, lumber_width("4x4"), height])
        rotate([90, 0, 90])
        rotate([0, 90, 0])
        bed_rail(width - 2 * lumber_width("4x4"));
    
    // Center support beam
    translate([lumber_width("4x4"), width/2 - lumber_width("2x6")/2, height])
        center_support(length - 2 * lumber_width("4x4"));
    
    // Support slats
    slat_spacing = (length - 2 * lumber_width("4x4")) / (num_slats + 1);
    for (i = [1:num_slats]) {
        translate([lumber_width("4x4") + i * slat_spacing - lumber_width("1x4")/2, 
                   lumber_width("4x4"), 
                   height + lumber_thickness("2x10") - lumber_thickness("1x4")])
            rotate([0, 0, 90])
            support_slat(width - 2 * lumber_width("4x4"));
    }
    
    // Headboard
    translate([0, lumber_width("4x4"), 0])
        rotate([90, 0, 0])
        headboard(width, headboard_h);
}

// Generate the bed frame
bed_frame(bed_length, bed_width, bed_height, headboard_height, mattress_support_slats);