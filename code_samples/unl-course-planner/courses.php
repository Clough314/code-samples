<?php

$codes = json_decode($_POST['codes']);
$rows = array();
foreach($codes as $code) {
    $sql = new mysqli("cse.unl.edu", "apages", "Wtpt4R", "apages");
    $qry = "SELECT c.title, c.description, c.prerequisite, c.creditHours, c.courseNum, s.subjectId, a1.aceNum AS aceNum1, a2.aceNum AS aceNum2 ".
        "FROM Course c JOIN Subject s ON c.subject_fk = s.subject_key ".
        "LEFT JOIN Ace AS a1 ON c.ace_1_fk = a1.ace_key ".
        "LEFT JOIN Ace AS a2 ON c.ace_2_fk = a2.ace_key ".
        "WHERE subjectId = ?";

    $qry = $sql->prepare($qry);
    $qry->bind_param("s", $code);
    $qry->execute();
    $result = $qry->get_result();
    //while($row = mysqli_fetch_assoc($result)) {
    //	echo $row["title"];
    //}
    while ($row = mysqli_fetch_assoc($result)) {
        $rows[] = array(
            'title' => $row['title'],
            'description' => $row['description'],
            'prerequisite' => $row['prerequisite'],
            'creditHours' => $row['creditHours'],
            'courseName' => $row['subjectId'],
            'courseNum' => $row['courseNum'],
            'ace1' => $row['aceNum1'],
            'ace2' => $row['aceNum2']
        );
    }
}
mysqli_close($sql);
echo json_encode($rows);
?>