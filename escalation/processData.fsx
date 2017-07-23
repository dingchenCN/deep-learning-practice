#r "./../packages/FSharp.Data/lib/net40/FSharp.Data.dll"
#r "./../packages/SQLProvider/lib/FSharp.Data.SqlProvider.dll"
open FSharp.Data
open FSharp.Data.Sql
open System.IO
open System
open System.Diagnostics
open System.Text.RegularExpressions

type DefectSchema = JsonProvider<"./defects_0.json">
type AuditsSchema = JsonProvider<"./defects_0_audits.json">

let (defectsFiles, auditsFiles) =
    Directory.GetFiles("../Raw")
    |> Array.groupBy (fun x -> if x.EndsWith("audits.json") then "Audits" else "Defects")
    |> Array.unzip
    |> fun (_, x) -> (x.[0], x.[1])

let GetFieldByName (fields:DefectSchema.Field[]) name =
    fields
    |> Array.tryFind (fun x -> x.Name.Equals(name, StringComparison.OrdinalIgnoreCase))

let ProcessFieldValues (field: DefectSchema.Field option) =
    match field with
    | Some f -> f.Values.[0].Value.String.Value
    | _ -> ""
let IsFieldValuesEmpty (field: DefectSchema.Field option) =
    if field.Value.Values.Length = 0 ||
       Regex.IsMatch(string field.Value.Values.[0],  "{\s*}") then
        true
    else
        false

let log message =
    let now = DateTime.Now.ToLongTimeString()
    printfn "%s: %s" now message
    File.AppendAllText("fetching.log", "\n"+now+": "+message)

let CreateDBSchema =
    ProcessStartInfo(__SOURCE_DIRECTORY__ + @"\..\GenertateProcessedDataSchema.bat")
    |> fun p -> p.WindowStyle <- ProcessWindowStyle.Hidden
                p.UseShellExecute <- true
                Process.Start(p) |> ignore
let [<Literal>] connectionString = "Data Source=" + __SOURCE_DIRECTORY__ + @"\..\ProcessedData.db;Version=3"
let [<Literal>] resolutionPath = __SOURCE_DIRECTORY__ + @"/../packages/System.Data.SQLite.Core/lib/net40/"
type SQLITESchema =
    SqlDataProvider<
        ConnectionString = connectionString,
        DatabaseVendor = Common.DatabaseProviderTypes.SQLITE,
        ResolutionPath = resolutionPath,
        IndividualsAmount = 1000,
        UseOptionTypes = false>
let sqliteContext = SQLITESchema.GetDataContext()


let Process() =
    // defectsFiles.Length-1
    for defectFile in defectsFiles.[0..defectsFiles.Length-1] do
        printfn "Processing: %s ..." defectFile
        DefectSchema.Load("..\\"+defectFile).Entities
        |> Array.filter (fun defect -> match GetFieldByName defect.Fields "user-27" with
                                       | Some x -> x.Values.[0].Value.String.Value.StartsWith("QCIM")
                                       | _ -> false)
        |> Array.iter
            (fun defect ->
                try
                    let row = sqliteContext.Main.Defects.Create()
                    row.Id <-
                        "id" |> GetFieldByName defect.Fields |> fun field -> field.Value.Values.[0].Value.String.Value |> int

                    row.GlobalId <-
                        "user-27" |> GetFieldByName defect.Fields |> ProcessFieldValues
                    row.Summary <-
                        "name" |> GetFieldByName defect.Fields |> ProcessFieldValues

                    row.Description <-
                         "description" |> GetFieldByName defect.Fields |> ProcessFieldValues

                    row.CurrentStatus <-
                        "status" |> GetFieldByName defect.Fields |> ProcessFieldValues
                        |> fun value -> match value with
                                        | "Awaiting Decision" -> 1
                                        | "Closed" -> 2
                                        | "Closed - No Change" -> 3
                                        | "Closed - No Problem" -> 4
                                        | "Deferred" -> 5
                                        | "Duplicate" -> 6
                                        | "Fixed" -> 7
                                        | "New" -> 8
                                        | "Open" -> 9
                                        | "Pending Support" -> 10
                                        | "Planned" -> 11
                                        | "Proposed Closed - No Change" -> 12
                                        | "Queued" -> 13
                                        | "Solution Accepted" -> 14
                                        | "Solution Delivered" -> 15
                                        | _ -> raise (Exception "not mapped status value")

                    row.Severity <-
                        "severity" |> GetFieldByName defect.Fields |> ProcessFieldValues
                        |> fun value -> match value with
                                        | "1 - Urgent" -> 1
                                        | "2 - High" -> 2
                                        | "3 - Medium" -> 3
                                        | "4 - Low" -> 4
                                        | _ -> raise (Exception "not mapped severity value")

                    row.Regression <-
                        "user-83" |> GetFieldByName defect.Fields |> ProcessFieldValues
                        |> fun value -> match value with
                                        | "Not a Regression" -> 0
                                        | "Not a Regression - Escaped Defect" -> 0
                                        | "Unknown" -> 0
                                        | "Legacy Feature Regression" -> 1
                                        | "New Feature Regression" -> 2
                                        | _ -> raise (Exception "not mapped regression value")

                    row.Reproducible <-
                        "reproducible" |> GetFieldByName defect.Fields |> ProcessFieldValues
                        |> fun value -> match value with
                                        | "N" -> 0
                                        | "Y" -> 1
                                        | _ -> raise (Exception "not mapped reproducible value")

                    row.AttachmentCounts <-
                        "attachment" |> GetFieldByName defect.Fields |> fun x -> match IsFieldValuesEmpty x with
                                                                                 | true -> 0
                                                                                 | _ -> x.Value.Values.Length

                    row.DurationDays <-
                        let createTime = "creation-time" |> GetFieldByName defect.Fields |> ProcessFieldValues |> DateTime.Parse
                        let closingDate = "closing-date" |> GetFieldByName defect.Fields |> ProcessFieldValues |> DateTime.Parse
                        closingDate - createTime
                        |> fun t -> t.TotalDays

                    row.Comments <-
                        "dev-comments" |> GetFieldByName defect.Fields |> ProcessFieldValues
                    row.CommentCounts <-
                        Regex.Matches(row.Comments, "<b>[^<,]*,\s*[\d]+-[\d]+-[\d]+\s*:\s*<\/b>").Count

                    row.EscalationLevel <-
                        "user-84" |> GetFieldByName defect.Fields |> ProcessFieldValues
                        |> fun x -> match x with
                                    | "N" -> 0
                                    | "Green" -> 0
                                    | "Y" -> 1
                                    | "Showstopper" -> 2
                                    | "Yellow" -> 3
                                    | "Red" -> 4
                                    | _ -> raise (Exception "not mapped escalation status")


                with
                    | e -> let id = "id" |> GetFieldByName defect.Fields |> ProcessFieldValues
                           sprintf "%s - Defect Id:%s: %s %s" (DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")) id e.Message e.StackTrace
                           |> log)

        try sqliteContext.SubmitUpdates()
        with | e -> sprintf "%s - Sumbit to db error. Defect file:%s: %s %s" (DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")) defectFile e.Message e.StackTrace
                    |> log
Process()