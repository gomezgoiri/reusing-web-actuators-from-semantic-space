@prefix : <http://example.org/light_scen#>.
@prefix http: <http://www.w3.org/2011/http#>.
@prefix ssn: <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>.
@prefix dbpedia: <http://dbpedia.org/resource/>.
@prefix dbpedia-owl: <http://dbpedia.org/ontology/>.
@prefix sweet: <http://sweet.jpl.nasa.gov/>.
@prefix ucum: <http://purl.oclc.org/NET/muo/ucum/>.
@prefix dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix frap: <http://purl.org/frap/>.
@prefix op: <http://www.w3.org/2000/10/swap/math#>.
@prefix lookfor: <http://pending.of/search/>.

:lightSensor a ssn:Sensor;
	    #ssn:observes sweet:Light ; # redundant: madeObservation and observedProperty defined
	    # ssn:onPlatform :adj_lamp . # redundant: inverse of attachedSystem
	    ssn:madeObservation :lobservation{{id}} .

:lobservation{{id}} #a  ssn:Observation ;
	ssn:observedProperty  sweet:Light ;
	# ssn:observedBy :lightSensor ; # redundant madeObservation
	ssn:observationResult :loresult{{id}} .
    
:loresult{{id}} ssn:hasValue :lvalue{{id}} .

:lvalue{{id}} a ssn:ObservationValue ;
    dul:isClassifiedBy  ucum:lux ;
    dul:hasDataValue {{value}} . 
