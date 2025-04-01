/*********************************************
 * OPL 22.1.1.0 Model
 * Author: Antoine Dardanne, Sébastien Chauviere, Théo Cudeville, Noé Florence
 * Creation Date: 4 mars 2024 at 15:03:06
 *********************************************/

//definire le nombre de nodes
int nbclients=11;
int nbvehicules=4;

// définir les parametres
// définir index
range clients=1..nbclients; //I l'ensemble des villes
range vehicules=1..nbvehicules; //I l'ensemble des vehicules

//c est le couts ou bien la distance entre deux villes; créer des nombres aléatoire
float d[i in clients][j in clients]=...;
float c[i in clients]=...;
float q[k in vehicules]=100;



//Variables de décision
dvar boolean x[clients][clients][vehicules]; //x est un variable boolean égale 1 si il visite de la ville i à j sinon 0
dvar int+ u[clients][vehicules]; // u est un variable pour éliminer les sous tours

minimize sum(i,j in clients , k in vehicules)  d[i][j]*x[i][j][k];


//objective function
subject
to{
//constraints

//chaque nœud est entré une fois par un vehicule.
c1:
forall (j in clients: j >1) sum(i in clients) sum(k in vehicules) x[i][j][k]==1;


c2:
forall (i in clients: i > 1, k in vehicules) sum(j in clients)  x[i][j][k] == sum(j in clients)  x[j][i][k];

//Chaque véhicule quitte le dépôt et y retourne
c3:
forall(k in vehicules) sum (j in clients)  x[1][j][k]==1;

c4:
//Contrainte pour ne dépasser la capacité du véhicule:
forall (k in vehicules) sum(i in clients) sum(j in clients ) c[i] * x[i][j][k] <= q[k];

//Contraintes pour éliminer les sous tours
c5:
forall (i,j in clients:  j > 1 , k in vehicules) u[i][k] - u[j][k] + (nbclients-nbvehicules) * x[i][j][k] <= (nbclients-nbvehicules-1);

}

execute {
    // Affichage des résultats
writeln("Déroulement des tournées : \n");

// Boucle sur les variables de décision x
	for (var k in vehicules) {
	    var currentCity = 1; // Départ de la première ville après le dépôt
	    writeln("Le vehicule ", k, " part du depot ");
	
	    var remainingCapacity = q[k];
	    var deliveredToDepot = false;
	    var deliveredAnything = false; // Variable pour vérifier si quelque chose a été livré
	
	    while (!deliveredToDepot) {
	        for (var j in clients) {
	            if (x[currentCity][j][k].solutionValue > 0.5) {
	                var nextCity = j;
	                if (nextCity == 1) {
	                    deliveredToDepot = true;
	                    if (!deliveredAnything) { // Si rien n'a été livré
	                        writeln(" Le véhicule ", k ," ne livre rien et retourne au depot \n");
	                    } else {
	                        writeln(" Le véhicule ", k ," retourne au depot \n");
	                    }
	                    break;
	                } else {
	                    deliveredAnything = true; // Indique qu'une livraison a été effectuée
	                    writeln("Le véhicule ", k, " part du client ", currentCity-1, " vers le client ", nextCity-1);
	                    currentCity = nextCity;
	                    remainingCapacity -= c[currentCity];
	                    writeln("    Quantite restante dans le vehicule ", k, ": ", remainingCapacity);
	                    break;
	                }
	            }
	        }
	    }
	}
}
