// Parametric bookshelf design
include <lumber_lib.scad>

// Default parameters
shelf_height = 72;    // 6 feet tall
shelf_width = 36;     // 3 feet wide
shelf_depth = 12;     // 1 foot deep
num_shelves = 5;      // Number of shelves including top and bottom
shelf_thickness = "1x12";  // Using 1x12 boards for shelves

// View mode: "assembled" or "exploded"
view_mode = "assembled";

// Module for vertical sides
module bookshelf_side(height, depth) {
    lumber(shelf_thickness, height);
}

// Module for shelves
module shelf(width) {
    lumber(shelf_thickness, width);
}

// Module for back support
module back_support(width, height, exploded = false) {
    exp_offset = exploded ? 5 : 0;
    
    // Using 1x4 boards for back support
    // Vertical supports
    support_spacing = width / 3;
    for (i = [0:1]) {
        x = (i + 1) * support_spacing;
        translate([
            x - lumber_width("1x4")/2,
            exploded ? -exp_offset * (i + 1) : 0,
            0
        ])
            lumber("1x4", height);
    }
    
    // Horizontal supports (top and bottom)
    for (i = [0:1]) {
        z = i == 0 ? lumber_width("1x4") : height - lumber_width("1x4") * 2;
        translate([
            0,
            exploded ? -exp_offset * (i + 3) : 0,
            z
        ])
            rotate([0, 90, 0])
            lumber("1x4", width);
    }
}

// Main bookshelf assembly
module bookshelf(height, width, depth, num_shelves, exploded = false) {
    shelf_spacing = (height - lumber_thickness(shelf_thickness)) / (num_shelves - 1);
    side_thickness = lumber_thickness(shelf_thickness);
    exp_offset = exploded ? 8 : 0;
    
    // Left side
    translate([exploded ? -exp_offset : 0, 0, 0])
        rotate([0, 0, 90])
        bookshelf_side(height, depth);
    
    // Right side
    translate([width - side_thickness + (exploded ? exp_offset : 0), 0, 0])
        rotate([0, 0, 90])
        bookshelf_side(height, depth);
    
    // Shelves
    for (i = [0:num_shelves-1]) {
        shelf_height = i * shelf_spacing;
        translate([
            side_thickness,
            exploded ? -exp_offset * 0.5 * (i % 2 == 0 ? 1 : -1) : 0,
            shelf_height + (exploded ? i * 2 : 0)
        ])
            rotate([0, 0, 0])
            shelf(width - 2 * side_thickness);
    }
    
    // Back support structure
    translate([
        side_thickness,
        depth - lumber_thickness("1x4") + (exploded ? exp_offset * 2 : 0),
        0
    ])
        back_support(width - 2 * side_thickness, height, exploded);
    
    // Optional: Add face frame for strength and aesthetics
    if (height > 48) {
        // Top rail
        translate([
            0,
            -lumber_thickness("1x2") - (exploded ? exp_offset : 0),
            height - lumber_width("1x2") + (exploded ? exp_offset : 0)
        ])
            rotate([0, 90, 0])
            lumber("1x2", width);
        
        // Bottom rail
        translate([
            0,
            -lumber_thickness("1x2") - (exploded ? exp_offset : 0),
            exploded ? -exp_offset : 0
        ])
            rotate([0, 90, 0])
            lumber("1x2", width);
    }
}

// Exploded view
module bookshelf_exploded(height, width, depth, num_shelves) {
    bookshelf(height, width, depth, num_shelves, true);
}

// Generate the bookshelf based on view mode
if (view_mode == "exploded") {
    bookshelf_exploded(shelf_height, shelf_width, shelf_depth, num_shelves);
} else {
    bookshelf(shelf_height, shelf_width, shelf_depth, num_shelves, false);
}