<?php
$email = $mysqli->real_escape_string($email);
$con->query("SELECT * FROM users WHERE email = '($email)'");
