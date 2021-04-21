<?php	
    $username = $_POST["username"];
    $password = $_POST["password"];
    $stmt = $mysqli->prepare("SELECT FROM login WHERE user=? AND pass=?");    
    $stmt->mysqli_bind_param("ss",$username,$password);
    $stmt->execute();
    $stmt->close();
    $mysqli->close();
?>