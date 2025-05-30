// Parametric workbench design with improved assembly
include <lumber_lib.scad>

// Default parameters
bench_length = 72;
bench_width = 24;
bench_height = 34;
top_thickness = 3;

// View mode: "assembled" or "exploded"
view_mode = "assembled";

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

// Main workbench assembly with better connections
module workbench(length, width, height, top_thick, exploded = false) {
    leg_inset = 4; // Inset legs from edges
    
    // Calculate actual top thickness based on lumber
    num_top_boards = ceil(width / lumber_width("2x6"));
    actual_top_width = num_top_boards * lumber_width("2x6");
    
    // Explosion offset for exploded view
    exp_offset = exploded ? 10 : 0;
    
    // Legs (4x4) - ensure they connect to top
    leg_positions = [
        [leg_inset, leg_inset, 0],
        [length - leg_inset - lumber_width("4x4"), leg_inset, 0],
        [leg_inset, width - leg_inset - lumber_width("4x4"), 0],
        [length - leg_inset - lumber_width("4x4"), width - leg_inset - lumber_width("4x4"), 0]
    ];
    
    for (i = [0:3]) {
        translate(exploded ? [
            leg_positions[i][0] + (i % 2) * exp_offset * (i < 2 ? -1 : 1),
            leg_positions[i][1] + (i < 2 ? -exp_offset : exp_offset),
            0
        ] : leg_positions[i])
            bench_leg(height);
    }
    
    // Top (multiple 2x6 boards) - directly on top of legs
    translate(exploded ? [0, 0, height + exp_offset * 2] : [0, 0, height - lumber_thickness("2x6")]) {
        for (i = [0:num_top_boards-1]) {
            translate([0, i * lumber_width("2x6") + (exploded ? i * 2 : 0), 0])
                rotate([0, 0, 0])
                top_board(length);
        }
    }
    
    // Long stretchers (2x4) - positioned to touch legs
    stretcher_height = height - 10; // Position 10" from bottom
    
    // Front long stretcher
    translate(exploded ? 
        [leg_inset, leg_inset + lumber_width("4x4") - exp_offset, stretcher_height] : 
        [leg_inset, leg_inset + lumber_width("4x4"), stretcher_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
    
    // Back long stretcher
    translate(exploded ? 
        [leg_inset, width - leg_inset - lumber_thickness("2x4") + exp_offset, stretcher_height] :
        [leg_inset, width - leg_inset - lumber_thickness("2x4"), stretcher_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
    
    // Short stretchers (2x4) - positioned to touch legs
    // Left short stretcher
    translate(exploded ?
        [leg_inset + lumber_width("4x4"), leg_inset - exp_offset, stretcher_height + exp_offset/2] :
        [leg_inset + lumber_width("4x4"), leg_inset, stretcher_height])
        rotate([90, 0, 90])
        stretcher("2x4", width - 2*leg_inset);
    
    // Right short stretcher  
    translate(exploded ?
        [length - leg_inset - lumber_thickness("2x4") + exp_offset, leg_inset - exp_offset, stretcher_height + exp_offset/2] :
        [length - leg_inset - lumber_thickness("2x4"), leg_inset, stretcher_height])
        rotate([90, 0, 90])
        stretcher("2x4", width - 2*leg_inset);
    
    // Bottom shelf stretchers - positioned to touch legs
    shelf_height = 6; // 6" from ground
    
    // Front bottom stretcher
    translate(exploded ?
        [leg_inset, leg_inset + lumber_width("4x4") - exp_offset, shelf_height - exp_offset/2] :
        [leg_inset, leg_inset + lumber_width("4x4"), shelf_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
    
    // Back bottom stretcher
    translate(exploded ?
        [leg_inset, width - leg_inset - lumber_thickness("2x4") + exp_offset, shelf_height - exp_offset/2] :
        [leg_inset, width - leg_inset - lumber_thickness("2x4"), shelf_height])
        rotate([90, 0, 0])
        stretcher("2x4", length - 2*leg_inset);
}

// Exploded view with labeled parts
module workbench_exploded(length, width, height, top_thick) {
    workbench(length, width, height, top_thick, true);
}

// Generate the workbench based on view mode
if (view_mode == "exploded") {
    workbench_exploded(bench_length, bench_width, bench_height, top_thickness);
} else {
    workbench(bench_length, bench_width, bench_height, top_thickness, false);
}