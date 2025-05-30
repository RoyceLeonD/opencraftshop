// Parametric workbench design
include <lumber_lib.scad>

// Default parameters
bench_length = 72;
bench_width = 24;
bench_height = 34;
top_thickness = 3;

// Module for workbench legs
module bench_leg(height) {
    lumber("4x4", height);
}

// Module for stretchers (horizontal supports)
module stretcher(lumber_type, length) {
    lumber(lumber_type, length);
}

// Module for top boards
module top_board(length) {
    lumber("2x6", length);
}

// Main workbench assembly
module workbench(length, width, height, top_thick) {
    leg_inset = 4; // Inset legs from edges
    
    // Calculate actual top thickness based on lumber
    num_top_boards = ceil(width / lumber_width("2x6"));
    actual_top_width = num_top_boards * lumber_width("2x6");
    
    // Legs (4x4)
    leg_positions = [
        [leg_inset, leg_inset, 0],
        [length - leg_inset - lumber_width("4x4"), leg_inset, 0],
        [leg_inset, width - leg_inset - lumber_width("4x4"), 0],
        [length - leg_inset - lumber_width("4x4"), width - leg_inset - lumber_width("4x4"), 0]
    ];
    
    for (pos = leg_positions) {
        translate(pos) bench_leg(height);
    }
    
    // Top (multiple 2x6 boards)
    translate([0, 0, height]) {
        for (i = [0:num_top_boards-1]) {
            translate([0, i * lumber_width("2x6"), 0])
                rotate([0, 0, 0])
                top_board(length);
        }
    }
    
    // Long stretchers (2x4)
    stretcher_height = height - 10; // Position 10" from bottom
    translate([leg_inset, leg_inset + lumber_width("4x4"), stretcher_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
    
    translate([leg_inset, width - leg_inset - lumber_thickness("2x4"), stretcher_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
    
    // Short stretchers (2x4)
    translate([leg_inset + lumber_width("4x4"), leg_inset, stretcher_height])
        rotate([90, 0, 90])
        stretcher("2x4", width - 2*leg_inset);
    
    translate([length - leg_inset - lumber_thickness("2x4"), leg_inset, stretcher_height])
        rotate([90, 0, 90])
        stretcher("2x4", width - 2*leg_inset);
    
    // Bottom shelf stretchers
    shelf_height = 6; // 6" from ground
    translate([leg_inset, leg_inset + lumber_width("4x4"), shelf_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
    
    translate([leg_inset, width - leg_inset - lumber_thickness("2x4"), shelf_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
}

// Generate the workbench
workbench(bench_length, bench_width, bench_height, top_thickness);