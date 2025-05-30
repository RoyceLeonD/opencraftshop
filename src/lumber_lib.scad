// Lumber dimension library
// Maps nominal sizes to actual dimensions

// Map nominal to actual dimensions [thickness, width]
function lumber_actual(nominal) = 
    nominal == "2x4" ? [1.5, 3.5] :
    nominal == "2x6" ? [1.5, 5.5] :
    nominal == "2x8" ? [1.5, 7.25] :
    nominal == "2x10" ? [1.5, 9.25] :
    nominal == "2x12" ? [1.5, 11.25] :
    nominal == "4x4" ? [3.5, 3.5] :
    nominal == "1x2" ? [0.75, 1.5] :
    nominal == "1x4" ? [0.75, 3.5] :
    nominal == "1x6" ? [0.75, 5.5] :
    nominal == "1x8" ? [0.75, 7.25] :
    nominal == "1x10" ? [0.75, 9.25] :
    nominal == "1x12" ? [0.75, 11.25] :
    [0, 0]; // default

// Standard lumber lengths in inches
function standard_lengths() = [96, 120, 144, 192]; // 8', 10', 12', 16'

// Helper function to get thickness
function lumber_thickness(nominal) = lumber_actual(nominal)[0];

// Helper function to get width
function lumber_width(nominal) = lumber_actual(nominal)[1];

// Module to create a lumber piece
module lumber(nominal, length) {
    dims = lumber_actual(nominal);
    cube([length, dims[1], dims[0]]);
}