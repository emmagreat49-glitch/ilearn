/**
 * iLEARN — Grade Analytics Engine
 * ═══════════════════════════════════════════════════════════════
 * Language  : Java 11+
 * Purpose   : Reads student quiz scores exported by the Flask
 *             backend, computes grades, rankings, and writes a
 *             formatted report to data_science/grade_report.json
 *
 * How it fits the project:
 *   Flask (Python) → exports scores to CSV
 *   GradeAnalyzer  → processes CSV, computes grades
 *   Flask          → reads JSON report, displays on analytics page
 *
 * Run standalone:
 *   javac java/GradeAnalyzer.java -d java/out
 *   java -cp java/out GradeAnalyzer data_science/scores.csv data_science/grade_report.json
 * ═══════════════════════════════════════════════════════════════
 */

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

public class GradeAnalyzer {

    // ─── Grade boundary model ───
    enum Grade {
        A_PLUS("A+", 90, 100, "Distinction — Outstanding performance"),
        A     ("A",  80,  89, "Distinction — Excellent understanding"),
        B     ("B",  70,  79, "Merit — Good grasp of material"),
        C     ("C",  60,  69, "Pass — Adequate understanding"),
        D     ("D",  50,  59, "Pass — Minimum acceptable"),
        F     ("F",   0,  49, "Fail — Further study required");

        final String label, remark;
        final int min, max;

        Grade(String label, int min, int max, String remark) {
            this.label  = label;
            this.min    = min;
            this.max    = max;
            this.remark = remark;
        }

        static Grade from(double score) {
            for (Grade g : values()) {
                if (score >= g.min && score <= g.max) return g;
            }
            return F;
        }
    }

    // ─── Student record ───
    static class StudentRecord {
        String username, fullName, course;
        double score;          // percentage 0–100
        int    lessonsCompleted, totalLessons;
        String completedAt;

        StudentRecord(String username, String fullName, String course,
                      double score, int lessonsCompleted, int totalLessons,
                      String completedAt) {
            this.username         = username;
            this.fullName         = fullName;
            this.course           = course;
            this.score            = score;
            this.lessonsCompleted = lessonsCompleted;
            this.totalLessons     = totalLessons;
            this.completedAt      = completedAt;
        }

        Grade grade()      { return Grade.from(score); }
        boolean passed()   { return score >= 50; }
        double gpa()       { return score / 25.0; }  // scale to 4.0
    }

    // ─── Analytics summary ───
    static class AnalyticsSummary {
        double mean, median, stdDev, min, max;
        int passCount, failCount, totalStudents;
        Map<String, Long> gradeDistribution = new LinkedHashMap<>();
        Map<String, Double> courseAverages  = new LinkedHashMap<>();
        List<StudentRecord> topStudents     = new ArrayList<>();
        List<StudentRecord> atRisk          = new ArrayList<>();
    }

    // ════════════════════════════════════════════════
    // MAIN
    // ════════════════════════════════════════════════

    public static void main(String[] args) throws Exception {
        String inputPath  = args.length > 0 ? args[0] : "data_science/scores.csv";
        String outputPath = args.length > 1 ? args[1] : "data_science/grade_report.json";

        System.out.println("╔══════════════════════════════════╗");
        System.out.println("║   iLEARN Grade Analyzer (Java)   ║");
        System.out.println("╚══════════════════════════════════╝");
        System.out.println("  Input  : " + inputPath);
        System.out.println("  Output : " + outputPath);

        List<StudentRecord> records = parseCSV(inputPath);

        if (records.isEmpty()) {
            System.out.println("  [WARN] No records found. Writing empty report.");
            writeEmptyReport(outputPath);
            return;
        }

        System.out.printf("  Records : %d students loaded%n", records.size());

        AnalyticsSummary summary = computeAnalytics(records);
        String json = buildJson(records, summary);

        Files.writeString(Path.of(outputPath), json);
        System.out.println("  ✅ Report written to " + outputPath);
        printConsoleTable(records, summary);
    }

    // ════════════════════════════════════════════════
    // CSV PARSER
    // ════════════════════════════════════════════════

    static List<StudentRecord> parseCSV(String path) throws Exception {
        List<StudentRecord> list = new ArrayList<>();
        Path p = Path.of(path);
        if (!Files.exists(p)) {
            System.out.println("  [INFO] No CSV file found at " + path + ". Using sample data.");
            return sampleData();
        }

        List<String> lines = Files.readAllLines(p);
        if (lines.size() < 2) return list;  // header only

        // Expected CSV: username,full_name,course,score,lessons_completed,total_lessons,completed_at
        for (int i = 1; i < lines.size(); i++) {
            String line = lines.get(i).trim();
            if (line.isEmpty()) continue;
            String[] cols = line.split(",", -1);
            if (cols.length < 6) continue;
            try {
                list.add(new StudentRecord(
                    cols[0].trim(),
                    cols[1].trim(),
                    cols[2].trim(),
                    Double.parseDouble(cols[3].trim()),
                    Integer.parseInt(cols[4].trim()),
                    Integer.parseInt(cols[5].trim()),
                    cols.length > 6 ? cols[6].trim() : ""
                ));
            } catch (NumberFormatException e) {
                System.out.println("  [WARN] Skipping malformed row " + i + ": " + line);
            }
        }
        return list;
    }

    // ════════════════════════════════════════════════
    // ANALYTICS ENGINE
    // ════════════════════════════════════════════════

    static AnalyticsSummary computeAnalytics(List<StudentRecord> records) {
        AnalyticsSummary s = new AnalyticsSummary();
        s.totalStudents = records.size();

        double[] scores = records.stream().mapToDouble(r -> r.score).toArray();
        Arrays.sort(scores);

        // Basic stats
        s.min    = scores[0];
        s.max    = scores[scores.length - 1];
        s.mean   = Arrays.stream(scores).average().orElse(0);
        s.median = scores.length % 2 == 0
            ? (scores[scores.length/2 - 1] + scores[scores.length/2]) / 2.0
            : scores[scores.length/2];

        double variance = Arrays.stream(scores)
            .map(x -> Math.pow(x - s.mean, 2))
            .average().orElse(0);
        s.stdDev = Math.sqrt(variance);

        s.passCount = (int) records.stream().filter(StudentRecord::passed).count();
        s.failCount = s.totalStudents - s.passCount;

        // Grade distribution
        for (Grade g : Grade.values()) {
            s.gradeDistribution.put(g.label,
                records.stream().filter(r -> r.grade() == g).count());
        }

        // Course averages
        records.stream()
            .collect(Collectors.groupingBy(r -> r.course,
                     Collectors.averagingDouble(r -> r.score)))
            .entrySet().stream()
            .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
            .forEach(e -> s.courseAverages.put(e.getKey(),
                         Math.round(e.getValue() * 100.0) / 100.0));

        // Top students (top 5 by score)
        s.topStudents = records.stream()
            .sorted(Comparator.comparingDouble((StudentRecord r) -> r.score).reversed())
            .limit(5)
            .collect(Collectors.toList());

        // At-risk students (failing, sorted by score ascending)
        s.atRisk = records.stream()
            .filter(r -> !r.passed())
            .sorted(Comparator.comparingDouble(r -> r.score))
            .collect(Collectors.toList());

        return s;
    }

    // ════════════════════════════════════════════════
    // JSON BUILDER (no external dependencies needed)
    // ════════════════════════════════════════════════

    static String buildJson(List<StudentRecord> records, AnalyticsSummary s) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\n");

        // Summary stats
        sb.append(String.format(
            "  \"summary\": {\n" +
            "    \"total_students\": %d,\n" +
            "    \"pass_count\": %d,\n" +
            "    \"fail_count\": %d,\n" +
            "    \"pass_rate\": %.1f,\n" +
            "    \"mean_score\": %.2f,\n" +
            "    \"median_score\": %.2f,\n" +
            "    \"std_dev\": %.2f,\n" +
            "    \"min_score\": %.1f,\n" +
            "    \"max_score\": %.1f\n" +
            "  },\n",
            s.totalStudents, s.passCount, s.failCount,
            s.totalStudents > 0 ? (s.passCount * 100.0 / s.totalStudents) : 0,
            s.mean, s.median, s.stdDev, s.min, s.max
        ));

        // Grade distribution
        sb.append("  \"grade_distribution\": {\n");
        s.gradeDistribution.forEach((grade, count) ->
            sb.append(String.format("    \"%s\": %d,\n", grade, count)));
        if (!s.gradeDistribution.isEmpty()) sb.setLength(sb.length() - 2);
        sb.append("\n  },\n");

        // Course averages
        sb.append("  \"course_averages\": {\n");
        s.courseAverages.forEach((course, avg) ->
            sb.append(String.format("    \"%s\": %.2f,\n",
                course.replace("\"", "'"), avg)));
        if (!s.courseAverages.isEmpty()) sb.setLength(sb.length() - 2);
        sb.append("\n  },\n");

        // Top performers
        sb.append("  \"top_students\": [\n");
        for (StudentRecord r : s.topStudents) {
            sb.append(String.format(
                "    {\"username\": \"%s\", \"full_name\": \"%s\", " +
                "\"course\": \"%s\", \"score\": %.1f, \"grade\": \"%s\"},\n",
                r.username, r.fullName.replace("\"", "'"),
                r.course.replace("\"", "'"), r.score, r.grade().label));
        }
        if (!s.topStudents.isEmpty()) sb.setLength(sb.length() - 2);
        sb.append("\n  ],\n");

        // At-risk students
        sb.append("  \"at_risk_students\": [\n");
        for (StudentRecord r : s.atRisk) {
            sb.append(String.format(
                "    {\"username\": \"%s\", \"full_name\": \"%s\", " +
                "\"score\": %.1f, \"grade\": \"%s\", \"remark\": \"%s\"},\n",
                r.username, r.fullName.replace("\"", "'"),
                r.score, r.grade().label, r.grade().remark));
        }
        if (!s.atRisk.isEmpty()) sb.setLength(sb.length() - 2);
        sb.append("\n  ],\n");

        // All records
        sb.append("  \"all_records\": [\n");
        for (int i = 0; i < records.size(); i++) {
            StudentRecord r = records.get(i);
            sb.append(String.format(
                "    {\"username\": \"%s\", \"full_name\": \"%s\", " +
                "\"course\": \"%s\", \"score\": %.1f, \"grade\": \"%s\", " +
                "\"passed\": %b, \"gpa\": %.2f, " +
                "\"lessons_completed\": %d, \"total_lessons\": %d}%s\n",
                r.username, r.fullName.replace("\"", "'"),
                r.course.replace("\"", "'"), r.score, r.grade().label,
                r.passed(), r.gpa(),
                r.lessonsCompleted, r.totalLessons,
                i < records.size() - 1 ? "," : ""));
        }
        sb.append("  ],\n");

        sb.append("  \"generated_by\": \"iLEARN GradeAnalyzer.java\",\n");
        sb.append("  \"java_version\": \"").append(
            System.getProperty("java.version")).append("\"\n");
        sb.append("}\n");

        return sb.toString();
    }

    // ════════════════════════════════════════════════
    // CONSOLE OUTPUT
    // ════════════════════════════════════════════════

    static void printConsoleTable(List<StudentRecord> records, AnalyticsSummary s) {
        System.out.println("\n  ┌────────────────────────────────────────────────────┐");
        System.out.println("  │              GRADE REPORT SUMMARY                 │");
        System.out.println("  ├────────────────────────────────────────────────────┤");
        System.out.printf( "  │  Total Students : %-32d│%n", s.totalStudents);
        System.out.printf( "  │  Mean Score     : %-32.2f│%n", s.mean);
        System.out.printf( "  │  Median Score   : %-32.2f│%n", s.median);
        System.out.printf( "  │  Std Deviation  : %-32.2f│%n", s.stdDev);
        System.out.printf( "  │  Pass Rate      : %-31.1f%%│%n",
            s.totalStudents > 0 ? (s.passCount * 100.0 / s.totalStudents) : 0);
        System.out.println("  ├────────────────────────────────────────────────────┤");
        System.out.println("  │  Grade Distribution                                │");
        s.gradeDistribution.forEach((grade, count) ->
            System.out.printf("  │    %-4s : %3d students%28s│%n", grade, count, ""));
        System.out.println("  └────────────────────────────────────────────────────┘");
    }

    static void writeEmptyReport(String path) throws Exception {
        Files.writeString(Path.of(path),
            "{\"summary\":{\"total_students\":0,\"pass_count\":0,\"fail_count\":0," +
            "\"pass_rate\":0,\"mean_score\":0,\"median_score\":0,\"std_dev\":0," +
            "\"min_score\":0,\"max_score\":0},\"grade_distribution\":{}," +
            "\"course_averages\":{},\"top_students\":[],\"at_risk_students\":[]," +
            "\"all_records\":[]}\n");
    }

    // ════════════════════════════════════════════════
    // SAMPLE DATA (used when no CSV is present)
    // ════════════════════════════════════════════════

    static List<StudentRecord> sampleData() {
        return Arrays.asList(
            new StudentRecord("alice",   "Alice Johnson",  "Python Programming",   88.0, 8, 8, "2025-11-15"),
            new StudentRecord("bob",     "Bob Smith",      "JavaScript",           72.5, 6, 8, "2025-11-14"),
            new StudentRecord("carol",   "Carol Okafor",   "CSS & Web Design",     95.0, 7, 7, "2025-11-13"),
            new StudentRecord("dan",     "Daniel Eze",     "Java Programming",     61.0, 5, 7, "2025-11-12"),
            new StudentRecord("eve",     "Eve Adeyemi",    "Data Science",         45.0, 3, 6, "2025-11-10"),
            new StudentRecord("frank",   "Frank Nwosu",    "Python Programming",   78.0, 7, 8, "2025-11-09"),
            new StudentRecord("grace",   "Grace Babatunde","JavaScript",           55.5, 5, 8, "2025-11-08"),
            new StudentRecord("henry",   "Henry Obi",      "CSS & Web Design",     82.0, 6, 7, "2025-11-07"),
            new StudentRecord("irene",   "Irene Chukwu",   "Java Programming",     38.0, 2, 7, "2025-11-06"),
            new StudentRecord("james",   "James Alabi",    "Data Science",         91.0, 6, 6, "2025-11-05")
        );
    }
}
