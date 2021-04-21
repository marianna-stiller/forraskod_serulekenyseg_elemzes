<?php
$users_name = $dbConnection->prepare('SELECT * FROM users WHERE name = ?');
$users_name->bind_param('s', $name); // 's' specifies the variable type => 'string'
$users_name->execute();
$result = $users_name->get_result();
while ($row = $result->fetch_assoc()) {
// do something with $row
}
?>