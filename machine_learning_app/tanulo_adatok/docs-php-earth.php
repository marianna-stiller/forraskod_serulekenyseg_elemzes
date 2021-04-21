<?php
// Get data is sent through url for example, http://example.com/get-user.php?id=1 OR id=2;
$id = $_GET['id'] ?? null;

// In your code you are executing your application as usual
$mysqli = new mysqli('localhost', 'db_user', 'db_password', 'db_name');

if ($mysqli->connect_error) {
    die('Connect Error (' . $mysqli->connect_errno . ') ' . $mysqli->connect_error);
}

// bump! sql injected code gets inserted here. Be careful to avoid such coding
// and use prepared statements instead
$query = "SELECT username, email FROM users WHERE id = ?";

$stmt = $mysqli->stmt_init();

if ($stmt->prepare($query)) {
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();
    while ($row = $result->fetch_array(MYSQLI_NUM)) {
        printf ("%s (%s)\n", $row[0], $row[1]);
    }
}
