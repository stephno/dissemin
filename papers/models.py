from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from papers.utils import nstr

# Information about the researchers and their groups
class Department(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

class ResearchGroup(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

class Researcher(models.Model):
    department = models.ForeignKey(Department)
    groups = models.ManyToManyField(ResearchGroup, blank=True)

    # DOI search
    last_doi_search = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=512, blank=True, null=True)
    last_status_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        first_name = Name.objects.filter(researcher_id=self.id).order_by('id').first()
        if first_name:
            return unicode(first_name)
        return "Anonymous researcher"

    @property
    def authors_by_year(self):
        return Author.objects.filter(name__researcher_id=self.id).order_by('-paper__year')
    @property
    def names(self):
        return self.name_set.order_by('id')
    @property
    def name(self):
        name = self.names.first()
        if name:
            return name
        else:
            return "Anonymous researcher"
    @property
    def aka(self):
        return self.names[:2]

class Name(models.Model):
    researcher = models.ForeignKey(Researcher, blank=True, null=True)
    first = models.CharField(max_length=256)
    last = models.CharField(max_length=256)
    unique_together = ('first','last')# TODO Two researchers with the same name is not supported
    def __unicode__(self):
        return '%s %s' % (self.first,self.last)
    @property
    def is_known(self):
        return self.researcher != None

# Papers matching one or more researchers
class Paper(models.Model):
    title = models.CharField(max_length=1024)
    fingerprint = models.CharField(max_length=64)
    year = models.IntegerField()
    last_modified = models.DateField(auto_now=True)
    def __unicode__(self):
        return self.title
    
class Author(models.Model):
    paper = models.ForeignKey(Paper)
    name = models.ForeignKey(Name)
    def __unicode__(self):
        return unicode(self.name)

# Publication of these papers (in journals or conference proceedings)
class Publication(models.Model):
    paper = models.ForeignKey(Paper)
    title = models.CharField(max_length=256)
    issue = models.CharField(max_length=64, blank=True, null=True)
    volume = models.CharField(max_length=64, blank=True, null=True)
    pages = models.CharField(max_length=64, blank=True, null=True)
    date = models.CharField(max_length=128, blank=True, null=True)
    def __unicode__(self):
        result = self.title
        if self.issue or self.volume or self.pages or self.date:
            result += ', '
        if self.issue:
            result += self.issue
        if self.volume:
            result += '('+self.volume+')'
        if self.issue or self.volume:
            result += ', '
        if self.pages:
            result += self.pages+', '
        if self.date:
            result += self.date
        return result

# Rough data extracted through dx.doi.org
class DoiRecord(models.Model):
    doi = models.CharField(max_length=1024, unique=True) # in theory, there is no limit
    about = models.ForeignKey(Paper)
    def __unicode__(self):
        return self.doi

# Rough data extracted through OAI-PMH
class OaiSource(models.Model):
    url = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    prefix_identifier = models.CharField(max_length=256)
    prefix_url = models.CharField(max_length=256)
    restrict_set = models.CharField(max_length=256, null=True, blank=True)

    # Fetching properties
    last_update = models.DateTimeField()
    last_status_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=512, null=True, blank=True)
    def __unicode__(self):
        return self.name

class OaiRecord(models.Model):
    source = models.ForeignKey(OaiSource)
    identifier = models.CharField(max_length=512, unique=True)
    url = models.CharField(max_length=1024)
    about = models.ForeignKey(Paper)
    def __unicode__(self):
        return self.identifier



