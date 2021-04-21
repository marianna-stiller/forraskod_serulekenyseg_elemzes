<?php
$ids = join(',', $ids);
$dbConn->GetAll("SELECT * FROM campaigns WHERE id IN ({$ids})");
