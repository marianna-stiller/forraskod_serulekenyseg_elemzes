/*
This file parses the test php code (toimport_vulnerabilities.php)
and convert it to AST (toimport_vulnerabilities_ast.txt).
*/

var fs = require('fs');
var path = require('path');
var engine = require('php-parser');
var util = require('util');

var parser = new engine({
  parser: {
    extractDoc: true,
    php7: true
  },
  ast: {
    withPositions: true
  }
});

var phpFile = fs.readFileSync('./tanulo_adatok/toimport_vulnerabilities.php');
var parsedFile = parser.parseCode(phpFile);
fs.writeFileSync('./tanulo_adatok/AST/toimport_vulnerabilities_ast.txt', JSON.stringify(parsedFile,null,2));