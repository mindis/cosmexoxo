var utils = require('../models/utils')
  , db = require('../models/dbConnect');

function testDisplayCategoryTree(err, result) {
  if (err) {
    console.log('Error in getAllCategories: ' + err);
    db.close();
    return;
  }
  var catTree = utils.displayCategoryTree(result, 1);
  console.log('displayCategoryTree result:');
  console.log(catTree);
  onFinished();
}

function onFinished() {
  console.log('Finished!');
  db.close();
}

// start tests by getting all categories
console.log('link_to results:')
console.log(utils.link_to('/categories/Eye Liner', 'Eye Liner products'));

db.getAllCategories(testDisplayCategoryTree);