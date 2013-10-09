@prefix : <http://example.org/lamp/>.
@prefix actuators:  <http://example.org/lamp/actuators/> .
@prefix measures: <http://example.org/lamp/actuators/light/>.
@prefix measure:  <http://example.org/lamp/actuators/light/{{id}}/>. # TODO redirect to the last on .
@prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#> .
@prefix ucum:  <http://purl.oclc.org/NET/muo/ucum/> .
@prefix sweet:  <http://sweet.jpl.nasa.gov/> .
@prefix dul:  <http://www.loa.istc.cnr.it/ontologies/DUL.owl#> .


measures:{{id}} a ssn:Observation ;
				ssn:observedProperty  sweet:Light ;
				ssn:observedBy actuators:light ; # redundant madeObservation
				ssn:observationResult measure:or .
    
measure:or ssn:hasValue measure:ov .

measure:ov a ssn:ObservationValue ;
    	   dul:isClassifiedBy  ucum:lux ;
           dul:hasDataValue {{value}} .