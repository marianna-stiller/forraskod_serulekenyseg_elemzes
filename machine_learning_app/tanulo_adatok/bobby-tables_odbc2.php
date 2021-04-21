<?php
$dbh = odbc_exec($conn, 'SELECT * FROM users WHERE email = ?', [$email]);
$sth = $dbh->prepare('SELECT * FROM users WHERE email = :email');
$sth->execute([':email' => $email]);
