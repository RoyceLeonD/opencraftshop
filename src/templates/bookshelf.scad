// Parametric bookshelf design
include <lumber_lib.scad>

// Default parameters
shelf_height = 72;    // 6 feet tall
shelf_width = 36;     // 3 feet wide
shelf_depth = 12;     // 1 foot deep
num_shelves = 5;      // Number of shelves including top and bottom
shelf_thickness = "1x12";  // Using 1x12 boards for shelves

// Module for vertical sides
module bookshelf_side(height, depth) {
    lumber(shelf_thickness, height);
}

// Module for shelves
module shelf(width) {
    lumber(shelf_thickness, width);
}

// Module for back support
module back_support(width, height) {
    // Using 1x4 boards for back support
    // Vertical supports
    support_spacing = width / 3;
    for (x = [support_spacing, 2 * support_spacing]) {
        translate([x - lumber_width("1x4")/2, 0, 0])
            lumber("1x4", height);
    }
    
    // Horizontal supports (top and bottom)
    for (z = [lumber_width("1x4"), height - lumber_width("1x4") * 2]) {
        translate([0, 0, z])
            rotate([0, 90, 0])
            lumber("1x4", width);
    }
}

// Main bookshelf assembly
module bookshelf(height, width, depth, num_shelves) {
    shelf_spacing = (height - lumber_thickness(shelf_thickness)) / (num_shelves - 1);
    side_thickness = lumber_thickness(shelf_thickness);
    
    // Left side
    translate([0, 0, 0])
        rotate([0, 0, 90])
        bookshelf_side(height, depth);
    
    // Right side
    translate([width - side_thickness, 0, 0])
        rotate([0, 0, 90])
        bookshelf_side(height, depth);
    
    // Shelves
    for (i = [0:num_shelves-1]) {
        shelf_height = i * shelf_spacing;
        translate([side_thickness, 0, shelf_height])
            rotate([0, 0, 0])
            shelf(width - 2 * side_thickness);
    }
    
    // Back support structure
    translate([side_thickness, depth - lumber_thickness("1x4"), 0])
        back_support(width - 2 * side_thickness, height);
    
    // Optional: Add face frame for strength and aesthetics
    if (height > 48) {
        // Top rail
        translate([0, -lumber_thickness("1x2"), height - lumber_width("1x2")])
            rotate([0, 90, 0])
            lumber("1x2", width);
        
        // Bottom rail
        translate([0, -lumber_thickness("1x2"), 0])
            rotate([0, 90, 0])
            lumber("1x2", width);
    }
}

// Generate the bookshelf
bookshelf(shelf_height, shelf_width, shelf_depth, num_shelves);