<?php

$input = $_GET['input'];

if ($input) {
    $db = mysqli_connect("localhost", "sec", "dubbelgeheim", "bookshop");

// Check connection
    if (mysqli_connect_errno()) {
        echo "Failed to connect to MySQL: " . mysqli_connect_error();
    }
    $escaper = real_escape_string($input);
    $statement = $db->prepare("SELECT * FROM productcomment WHERE ProductId = ? LIMIT 1");
    $statement->bind_param("s", $escaper);
    $statement->execute();
    $result = $statement->get_result();
    $statement->close();
    $count = $result->num_rows;
    if ($count > 0) {
        while ($row = $result->fetch_assoc()) {
            echo "Product:" . $row['ProductId'] . "<br>";
            echo "Annotation:" . $row['Comment'] . "<br>";
            echo "TestOK!<br>";
        }
    } 
    else {
        echo 'No record!';
    }
    $result->free();
    $db->close();
}
?>