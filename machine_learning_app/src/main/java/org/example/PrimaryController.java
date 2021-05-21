package org.example;

import javafx.beans.binding.Bindings;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.chart.PieChart;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Hyperlink;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.control.TextArea;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.awt.*;
import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Date;
import java.util.ResourceBundle;

public class PrimaryController implements Initializable {
    @FXML
    public Label result;
    @FXML
    public PieChart piechart;
    @FXML
    public Button button2;
    @FXML
    public Button button3;
    @FXML
    public Label rtime;
    @FXML
    public Label describe1;
    @FXML
    public ProgressBar progress;
    @FXML
    public Label progress_no;
    @FXML
    public Hyperlink prevent_more;
    @FXML
    public Hyperlink sqli_more;
    @FXML
    public TextArea the_code;

    public double vulnerable;
    public double notvulnerable;
    public Process p1;
    public int pc1;
    public Process p2;
    public int pc2;
    public Process p3;
    public int pc3;
    public Process p4;

    public boolean isWindows() {
        if(System.getProperty("os.name").toLowerCase().startsWith("windows")){
            return true; // windows
        } else {
            return false; // linux
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        ArrayList<String> list = null;
        Date before_date = new Date();
        String line;
        String s1 = null;
        String l1 = null;
        String s2 = null;
        String l2 = null;
        String s3 = null;
        String l3 = null;
        long before_timeMilli = before_date.getTime();
        try {
            p1 = Runtime.getRuntime().exec("node parser.js");
            pc1 = p1.waitFor();
            BufferedReader p1err = new BufferedReader(new InputStreamReader(p1.getErrorStream()));
            while ((s1 = p1err.readLine()) != null) {
                l1 += s1 + '\n';
            }
            if(isWindows()) {
                p2 = Runtime.getRuntime().exec("py tokenizer.py");
                pc2 = p2.waitFor();
                BufferedReader p2err = new BufferedReader(new InputStreamReader(p2.getErrorStream()));
                while ((s2 = p2err.readLine()) != null) {
                    l2 += s2 + '\n';
                }
                p3 = Runtime.getRuntime().exec("py vectorizer.py");
                pc3 = p3.waitFor();
                BufferedReader p3err = new BufferedReader(new InputStreamReader(p3.getErrorStream()));
                while ((s3 = p3err.readLine()) != null) {
                    l3 += s3 + '\n';
                }
            } else {
                p2 = Runtime.getRuntime().exec("python3 tokenizer.py");
                pc2 = p2.waitFor();
                BufferedReader p2err = new BufferedReader(new InputStreamReader(p2.getErrorStream()));
                while ((s2 = p2err.readLine()) != null) {
                    l2 += s2 + '\n';
                }
                p3 = Runtime.getRuntime().exec("python3 vectorizer.py");
                pc3 = p3.waitFor();
                BufferedReader p3err = new BufferedReader(new InputStreamReader(p3.getErrorStream()));
                while ((s3 = p3err.readLine()) != null) {
                    l3 += s3 + '\n';
                }
            }

            if(pc1!=0 || pc2!=0 || pc3!=0) {
                Alert alert = new Alert(AlertType.ERROR);
                alert.setHeaderText("Valami probléma van!");
                alert.setContentText("Ellenőrizd a függőségeket és kattints a 'Vissza' gombra új programkód megadásához.");

                TextArea textArea1 = new TextArea(l1);
                textArea1.setEditable(false);
                textArea1.setWrapText(true);
                textArea1.setMaxHeight(70);
                textArea1.setMaxWidth(Double.MAX_VALUE);
                TextArea textArea2 = new TextArea(l2);
                textArea2.setEditable(false);
                textArea2.setWrapText(true);
                textArea2.setMaxHeight(70);
                textArea2.setMaxWidth(Double.MAX_VALUE);
                TextArea textArea3 = new TextArea(l3);
                textArea3.setEditable(false);
                textArea3.setWrapText(true);
                textArea3.setMaxHeight(70);
                textArea3.setMaxWidth(Double.MAX_VALUE);

                GridPane expContent = new GridPane();
                expContent.setMaxWidth(Double.MAX_VALUE);
                expContent.add(textArea1, 0, 0);
                expContent.add(textArea2, 0, 1);
                expContent.add(textArea3, 0, 2);
                alert.getDialogPane().setExpandableContent(expContent);
                alert.showAndWait();
            } else {
                if(isWindows()) {
                    p4 = Runtime.getRuntime().exec("py trainer.py -x testX.npy -y testy.npy -z toimportX.npy");
                } else {
                    p4 = Runtime.getRuntime().exec("python3 trainer.py -x testX.npy -y testy.npy -z toimportX.npy");
                }
                InputStream is = p4.getInputStream();
                InputStreamReader isr = new InputStreamReader(is);
                BufferedReader br = new BufferedReader(isr);

                list = new ArrayList<>();
                while ((line = br.readLine()) != null) {
                    list.add(line);
                }
                progress.setProgress(100);
                progress_no.setText(progress.getProgress() +"%");
                vulnerable = Double.parseDouble(list.get(list.size()-2))*100;
                notvulnerable = Double.parseDouble(list.get(list.size()-1))*100;

                Date after_date = new Date();
                long after_timeMilli = after_date.getTime();
                long runtime_in_mili = after_timeMilli - before_timeMilli;
                int runtime_in_sec = (int)((runtime_in_mili / 1000) % 60);
                rtime.setText(runtime_in_sec +" mp");
        
                var fileName = "tanulo_adatok/toimport_vulnerabilities.php";
                try (BufferedReader brr = new BufferedReader(
                        new FileReader(fileName, StandardCharsets.UTF_8))) {
                    var sb = new StringBuilder();
                    String lines;
                    while ((lines = brr.readLine()) != null) {
                        sb.append(lines);
                        sb.append(System.lineSeparator());
                    }
                    the_code.setText(String.valueOf(sb));
                } catch (IOException e) {
                    e.printStackTrace();
                }
                assert list != null;
                ObservableList<PieChart.Data> pieChartData = FXCollections.observableArrayList(
                                new PieChart.Data("Sérülékeny", Math.round(vulnerable)),
                                new PieChart.Data("Nem sérülékeny", Math.round(notvulnerable)));
                piechart.setData(pieChartData);
                pieChartData.forEach(data -> {
                    data.nameProperty().bind(Bindings.concat(data.getName()," [",data.pieValueProperty(),"%]"));
                    if(vulnerable > 50) {
                        piechart.getStylesheets().add("css/style.css");
                    } else {
                        piechart.getStylesheets().add("css/style2.css");
                    }
                });
                describe1.setText("A program "+Math.round(vulnerable)+"%-os (pontosabban "+vulnerable+"%-os) valószínűségűre állapította meg a kód sérülékenységét SQL Injection-el szemben.");        
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void back() throws IOException {
        Stage stage = (Stage) button2.getScene().getWindow();
        stage.close();

        Parent root = FXMLLoader.load(getClass().getResource("first.fxml"));
        Scene scene = new Scene(root);
        stage.setScene(scene);
        stage.show();
    }

    public void close() {
        Stage stage = (Stage) button3.getScene().getWindow();
        stage.close();
    }

    public void openWeb() {
        prevent_more.setOnAction(actionEvent -> {
            try {
                Desktop.getDesktop().browse(new URI("https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"));
            } catch (IOException | URISyntaxException e) {
                e.printStackTrace();
            }
        });
    }

    public void openWeb2() {
        sqli_more.setOnAction(actionEvent -> {
            try {
                Desktop.getDesktop().browse(new URI("https://owasp.org/www-community/attacks/SQL_Injection"));
            } catch (IOException | URISyntaxException e) {
                e.printStackTrace();
            }
        });
    }
}
