// Function that transposes a 2D array (matrix)
function transpose(matrix) {
  // Check if matrix is empty
  if (!matrix || matrix.length === 0) {
    return [];
  }
  
  // Get the number of rows and columns
  const rows = matrix.length;
  const cols = matrix[0].length;
  
  // Create a new matrix with swapped dimensions
  const result = [];
  
  // Iterate through columns of original matrix
  for (let col = 0; col < cols; col++) {
    const newRow = [];
    // Iterate through rows of original matrix
    for (let row = 0; row < rows; row++) {
      newRow.push(matrix[row][col]);
    }
    result.push(newRow);
  }
  
  return result;
}

// Test Data
const testData = [
  [1, 2, 3],
  [4, 5, 6]
];

// Test the function
console.log("Original Matrix:");
console.log(testData);

console.log("\nTransposed Matrix:");
const transposed = transpose(testData);
console.log(transposed);

// Expected output: [[1, 4], [2, 5], [3, 6]]

module.exports = transpose;
