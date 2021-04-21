<?php
$stmt = odbc_prepare( $conn, 'SELECT * FROM users WHERE email = ?' );
$success = odbc_execute( $stmt, [$email] );
