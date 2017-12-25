// Package web provide main application router.
package web

import (
	"log"
	"net/http"
	"os"

	"github.com/yaptide/app/config"
	"github.com/yaptide/app/web/auth"
	"github.com/yaptide/app/web/projects"
	"github.com/yaptide/app/web/server"
	"github.com/yaptide/app/web/simulation"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

// NewRouter create main router, which define root routes.
func NewRouter(config *config.Config) http.Handler {
	router := mux.NewRouter()
	context, err := server.NewContext(config)
	if err != nil {
		log.Printf("server.NewContext(config) fatal error: %s\n", err.Error())
		log.Println("Probably config is incorrect")
		log.Println("Terminating application")
		os.Exit(1)
	}

	authRouter := router.PathPrefix("/auth").Subrouter()
	auth.HandleAuth(authRouter, context)

	projectsRouter := router.PathPrefix("/projects").Subrouter()
	projects.HandleProject(projectsRouter, context)

	simulationRouter := router.PathPrefix("/simulation").Subrouter()
	simulation.HandleSimulation(simulationRouter, context)

	router.Handle("/configuration", &getConfigurationHandler{Context: context, Config: config}).
		Methods(http.MethodGet)

	//router.PathPrefix("/").Handler(http.FileServer(http.Dir(config.StaticDirectory)))

	return handlers.CORS(
		handlers.AllowedHeaders([]string{"content-type", "x-auth-token"}),
		handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE"}),
	)(router)
}
