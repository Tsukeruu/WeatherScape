package main

import(
	"github.com/charmbracelet/log"
	"os"
)

type errors interface{
	invalidlog() string
	FailedRequest() string
	InvalidSeverity() string
}

type validerrors struct {
	msg string
}

type CustomMsg struct {
	msg string
}

func (v *validerrors) invalidlog() string {
	v.msg = "Invalid log method!"
	log.Error(v.msg)
	return v.msg
}


func (v *validerrors) FailedRequest() string {
	v.msg = "Unable to make a GET request at wttr.in [Likely due to an issue in wttr.in or your internet]"
	log.Error(v.msg)
	return v.msg
}

func (v *validerrors) InvalidSeverity() string {
	v.msg = "Invalid severity for custom logging provided"
	log.Error(v.msg)
	return v.msg
}


func (v *CustomMsg) CustomLog() {
	var valid errors
	var Severity string = os.Args[3]
	valid = &validerrors{}
	v.msg = os.Args[2]
	switch Severity {
	case "Info":
		log.Info(v.msg)
	case "Error":
		log.Error(v.msg)
	case "Warn":
		log.Warn(v.msg)
	case "Debug":
		log.Debug(v.msg)
	default:
		valid.InvalidSeverity()
	}
}

func main() {
	var valid errors = &validerrors{}
	var custom CustomMsg
	arg := os.Args[1]
	log.SetLevel(log.DebugLevel)
	if arg == "Success" {
		log.Info("Sucessfully made a GET request at wttr.in!")
	} else if arg =="Fail" {
		valid.FailedRequest()
	} else if arg == "Custom" {
		custom.CustomLog()
	} else {
		valid.invalidlog()
	}
}
