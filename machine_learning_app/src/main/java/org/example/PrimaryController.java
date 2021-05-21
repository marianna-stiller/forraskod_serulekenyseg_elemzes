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
import javafx.scene.layout.Region;
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

    public String op() {
        if(System.getProperty("os.name").toLowerCase().startsWith("windows")){
            return "windows"; // windows
        } else if(System.getProperty("os.name").toLowerCase().startsWith("windows")) {
            return "linux"; // linux
        }
        return "A(z) "+System.getProperty("os.name")+" operációs rendszer nem támogatott";
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        ArrayList<String> list = null;
        Date before_date = new Date();
        String line;
        long before_timeMilli = before_date.getTime();
        try {
            p1 = Runtime.getRuntime().exec("node parser.js");
            pc1 = p1.waitFor();
            if(op()=="windows") {
                p2 = Runtime.getRuntime().exec("py tokenizer.py");
                pc2 = p2.waitFor();
                p3 = Runtime.getRuntime().exec("py vectorizer.py");
                pc3 = p3.waitFor();
            } else if(op()=="linux"){
                p2 = Runtime.getRuntime().exec("python3 tokenizer.py");
                pc2 = p2.waitFor();
                p3 = Runtime.getRuntime().exec("python3 vectorizer.py");
                pc3 = p3.waitFor();
            } else {
                System.out.println(op());
            }
            if(pc1!=0 || pc2!=0 || pc3!=0) {
                Alert alert = new Alert(AlertType.ERROR);
                alert.setHeaderText("A megadott kóddal valami probléma van!");
                alert.setContentText("Kérlek ellenőrizd a helyességét és kattints a 'Vissza' gombra új programkód megadásához.");
                alert.getDialogPane().setMinHeight(Region.USE_PREF_SIZE);
                alert.showAndWait();
            } else {
                if(op()=="windows") {
                    p4 = Runtime.getRuntime().exec("py trainer.py -x testX.npy -y testy.npy -z toimportX.npy");
                } else if(op()=="linux"){
                    p4 = Runtime.getRuntime().exec("python3 trainer.py -x testX.npy -y testy.npy -z toimportX.npy");
                } else {
                    System.out.println(op());
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
