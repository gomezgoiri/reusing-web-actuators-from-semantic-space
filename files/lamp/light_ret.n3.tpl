@prefix : <http://example.org/>.
@prefix actuators: <http://example.org/lamp/actuators/>.
@prefix measures: <http://example.org/lamp/actuators/light/>. # TODO redirect to the last one
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


# Light actuator of the adjustable lamp
# sth/lamp/actuators/light

      
actuators:light a ssn:Sensor;
  ssn:observes sweet:Light ; # redundant: madeObservation and observedProperty defined
  ssn:onPlatform :lamp . # redundant: inverse of attachedSystem
  lookfor:last measures:last .


{% for id in measures %}
actuators:light ssn:madeObservation measures:{{ id }} .
{% endfor %}