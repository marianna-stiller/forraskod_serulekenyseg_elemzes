<?php
$users_name = $pdo->prepare('SELECT * FROM employees WHERE name = :name');
$users_name->execute(array('name' => $name));
foreach ($users_name as $row) {
// do something with $row
}
?>