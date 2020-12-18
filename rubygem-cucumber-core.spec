%global gem_name cucumber-core
Name:                rubygem-%{gem_name}
Version:             3.2.0
Release:             2
Summary:             Core library for the Cucumber BDD app
License:             MIT
URL:                 https://cucumber.io
Source0:             https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:             https://github.com/cucumber/cucumber-ruby-core/archive/v%{version}.tar.gz
BuildRequires:       ruby(release) rubygems-devel ruby rubygem(gherkin) rubygem(rspec)
BuildRequires:       rubygem(kramdown) rubygem(cucumber-tag_expressions) rubygem(backports)
BuildRequires:       rubygem(kramdown-parser-gfm)
BuildArch:           noarch
%description
Core library for the Cucumber BDD app.

%package doc
Summary:             Documentation for %{name}
Requires:            %{name} = %{version}-%{release}
BuildArch:           noarch
%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1
%gemspec_remove_dep -s ../%{gem_name}-%{version}.gemspec -g gherkin '>= 5.0.0'
%gemspec_add_dep -s ../%{gem_name}-%{version}.gemspec -g gherkin '>= 4.1.0'

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/cucumber-ruby-core-%{version}/spec spec
for file in $(grep -Rl unindent spec); do
  sed -i "/require 'unindent'/ s/^/#/" "${file}"
  sed -i '/^ *expect.*unindent$/ i \pending' "${file}"
done
LANG=C.UTF-8 rspec -rkramdown/parser/gfm spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md

%changelog
* Tue Dec 15 2020 chengzihan <chengzihan2@huawei.com> -3.2.0-2
- add BuildRequires: rubygem(kramdown-parser-gfm) fix compiling problem

* Wed Aug 19 2020 fanjiachen <fanjiachen3@huawei.com> - 3.2.0-1
- package init
