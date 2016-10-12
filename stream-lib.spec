%{?scl:%scl_package stream-lib}
%{!?scl:%global pkg_name %{name}}

# NB: this package includes a forked version of Bloom filter code
# from Apache Cassandra.  FPC has granted a bundling exception since
# it is a fork; see https://fedorahosted.org/fpc/ticket/401 and
# http://meetbot.fedoraproject.org/fedora-meeting-1/2014-03-20/fedora-meeting-1.2014-03-20-17.05.html

%global commit 214c92595d5be3a1cedc881b50231ccb34862074
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           %{?scl_prefix}stream-lib
Version:        2.6.0
Release:        8%{?dist}
Summary:        Stream summarizer and cardinality estimator
License:        ASL 2.0
URL:            https://github.com/addthis/%{pkg_name}/
Source0:        https://github.com/addthis/%{pkg_name}/archive/%{commit}/%{pkg_name}-%{commit}.tar.gz
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)
# remove for scl package because of missing dependency
%{!?scl:BuildRequires:  mvn(it.unimi.dsi:fastutil)}
# missing test dependencies
#BuildRequires:  mvn(colt:colt)
#BuildRequires:  mvn(com.googlecode.charts4j:charts4j)
#BuildRequires:  mvn(org.apache.mahout:mahout-math)
%{?scl:Requires: %scl_runtime}

%description
A Java library for summarizing data in streams for which it is
infeasible to store all events. More specifically, there are classes
for estimating: cardinality (i.e. counting things); set membership;
top-k elements and frequency. One particularly useful feature is that
cardinality estimators with compatible configurations may be safely
merged.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -qn %{pkg_name}-%{commit}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Unneeded plugin
%pom_remove_plugin org.apache.maven.plugins:maven-shade-plugin pom.xml
# Unneeded task
%pom_remove_plugin :maven-source-plugin
# Fix doclint issues
%pom_remove_plugin :maven-javadoc-plugin

# remove missing dependency for scl package
%{?scl:%pom_remove_dep it.unimi.dsi:fastutil}
%{?scl:EOF}

# remove file requiring missing dependency
%{?scl:rm src/main/java/com/clearspring/analytics/stream/quantile/QDigest.java}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# tests are skipped due to missing test dependencies
%mvn_build -f 
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.mdown
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Oct 12 2016 Tomas Repik <trepik@redhat.com> - 2.6.0-8
- use standard SCL macros

* Tue Aug 23 2016 Tomas Repik <trepik@redhat.com> - 2.6.0-7
- remove unneeded missing dependency for scl package

* Wed Aug 10 2016 Tomas Repik <trepik@redhat.com>
- scl conversion

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 04 2015 gil cattaneo <puntogil@libero.it> 2.6.0-4
- Fix FTBFS RHBZ#1240033
- Introduce license macro

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 William Benton <willb@redhat.com> - 2.6.0-1
- Initial packaging
