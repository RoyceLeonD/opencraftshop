// Parametric storage bench / window bench design
include <lumber_lib.scad>

// Default parameters
bench_length = 48;
bench_width = 18;
bench_height = 18;
storage_depth = 14;

// View mode: "assembled" or "exploded"
view_mode = "assembled";

// Module for bench frame
module bench_frame(length, width, height) {
    // Corner posts (2x4)
    corner_offset = lumber_width("2x4");
    
    // Vertical posts
    for (x = [0, length - corner_offset]) {
        for (y = [0, width - corner_offset]) {
            translate([x, y, 0])
                lumber("2x4", height);
        }
    }
    
    // Top frame - long sides
    for (y = [0, width - corner_offset]) {
        translate([0, y, height - lumber_thickness("2x4")])
            rotate([0, 90, 0])
            lumber("2x4", length);
    }
    
    // Top frame - short sides
    for (x = [0, length - corner_offset]) {
        translate([x, corner_offset, height - lumber_thickness("2x4")])
            rotate([0, 90, 90])
            lumber("2x4", width - 2 * corner_offset);
    }
    
    // Bottom frame - long sides
    for (y = [0, width - corner_offset]) {
        translate([0, y, lumber_width("2x4")])
            rotate([0, 90, 0])
            lumber("2x4", length);
    }
    
    // Bottom frame - short sides
    for (x = [0, length - corner_offset]) {
        translate([x, corner_offset, lumber_width("2x4")])
            rotate([0, 90, 90])
            lumber("2x4", width - 2 * corner_offset);
    }
}

// Module for storage bench top
module bench_top(length, width) {
    // Using 1x6 boards for the top
    num_boards = ceil(width / lumber_width("1x6"));
    
    for (i = [0:num_boards-1]) {
        translate([0, i * lumber_width("1x6"), 0])
            lumber("1x6", length);
    }
}

// Module for storage compartment bottom
module storage_bottom(length, width) {
    // Plywood sheet (3/4" thick)
    cube([length, width, 0.75]);
}

// Main storage bench assembly
module storage_bench(length, width, height, storage_depth) {
    // Frame
    bench_frame(length, width, height);
    
    // Top
    translate([0, 0, height - lumber_thickness("1x6")])
        bench_top(length, width);
    
    // Storage bottom (raised for storage space)
    bottom_height = height - storage_depth;
    translate([lumber_width("2x4"), lumber_width("2x4"), bottom_height])
        storage_bottom(
            length - 2 * lumber_width("2x4"), 
            width - 2 * lumber_width("2x4")
        );
    
    // Optional: Add dividers for storage compartments
    if (length > 36) {
        // Middle divider
        translate([length/2 - lumber_thickness("1x4")/2, lumber_width("2x4"), bottom_height])
            rotate([0, 0, 90])
            lumber("1x4", width - 2 * lumber_width("2x4"));
    }
}

// Generate the storage bench
storage_bench(bench_length, bench_width, bench_height, storage_depth);