[33mcommit 8198490f16d5891e35b543b0f9302768c6f7e1a2[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Mon Feb 23 09:06:32 2015 -0800

    removed css for text in hive plot

[33mcommit 5e1ada8ffb5ea1ac0be976de5ffe3c7528cffac3[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Feb 9 09:41:06 2015 -0800

    Fixed some misleading comments and the hive plot labels for scale panels

[33mcommit f5992659fa58b2d0cac3667bcf2806147de8dc28[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Feb 9 09:09:12 2015 -0800

    Anchoring of axis labeled text now depends on coordinates to avoid overlap

[33mcommit eee6a447fa24051b988034201d64353e46907863[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Feb 9 08:25:16 2015 -0800

    cleaned up a few things associated with ranked scales

[33mcommit f971cf2b6345e8a27c7293bdd06903a57b0b6c34[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sun Feb 8 23:38:15 2015 -0800

    Nodes can now be positioned along axes using a rank type scale to avoid occlusion

[33mcommit 11e7f7dc9781c4d88de95366a84e36625957e056[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sun Feb 8 10:58:06 2015 -0800

    Fixed equality signs for axis labels

[33mcommit 610da557d54036b19548dec6cb39d3856ffe55c3[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sun Feb 8 10:51:40 2015 -0800

    Fixed even scale axis binning for interger values

[33mcommit d29f1218a3510a118110df5e53cab799ff6b4c64[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sun Feb 8 10:08:33 2015 -0800

    restructured script that builds degree distribution

[33mcommit 70476d43a106ca5f01c84e38f3e9a8c2efb2fcda[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Fri Feb 6 16:11:50 2015 -0800

    Made new panels to show different degree scales

[33mcommit c1687c9ff45de3765d53085910c5c6bd01fdea58[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Fri Feb 6 13:37:35 2015 -0800

    fixed the scale, legends and barchart to line

[33mcommit a4bb4eb40d8b05fef2c6ac5ef8b974adf3b427e8[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Fri Feb 6 12:01:01 2015 -0800

    Created a script to build two networks and plot their degree distribution using networkx and pretty plot lib

[33mcommit 86a318b655f69af183ebf77a4a6b3b006683047f[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Feb 3 17:12:54 2015 -0800

    fixed position of axis labels, fixed bug when cut off of even scale is the smallest value, and changed the equality signs to reflect the correct relationships

[33mcommit cb10857243cae15c07f4bd3c7ebc7b097e761d38[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Feb 3 15:01:58 2015 -0800

    Fixed sorting method for quantitative values, now sorting numerically when appropriate instead of lexicographically. This fixes the bug in assignment nodes using an even distribution

[33mcommit 6c5654ee6d1dc1da1398d6a6ad84d5c2ad478dc5[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Jan 20 21:23:13 2015 -0800

    removed the attempt at queueing tasks. Click feature works again

[33mcommit d638dc4e1bf0c8e569591ccef58bcd6afde1e929[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Jan 20 14:49:54 2015 -0800

    network_simulation script can now plot simulation by treatment or by centrality measure. Y-axis represents the relative size of the largest component left

[33mcommit a03e0f06c9426a474645a67675c6321b34d227ff[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sun Jan 18 16:59:54 2015 -0800

    modularized and finalized some aesthetic details of plotting multiple network simulations with several treatments

[33mcommit 011edbf457df66698bc3a23fdc07d6dbab7362a6[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sun Jan 18 11:40:11 2015 -0800

    multiplot (with several networks) and single plots of robustness simulations complete

[33mcommit d3956c40a710637d516a9b70e71cfde04bcf55c5[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sat Jan 17 23:44:39 2015 -0800

    started plotting the simulations using prettyplotlib. **ongoing**

[33mcommit 2a6b61d2b811c925def44bfd17e21303d1dcbf70[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Sat Jan 17 11:32:22 2015 -0800

    new file that runs attack simulations on networks given ordered nodes by properties

[33mcommit d37a714017b0c290862614e7adcdbae0ba64b6c4[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Thu Jan 15 16:44:48 2015 -0800

    cleaned up some things

[33mcommit eef2c1395ac14451cf51fb8eb1d18c376c64e110[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Thu Jan 15 13:45:05 2015 -0800

    Refit some items in the control panel

[33mcommit fa2b9027e1a3e5c5931c411199c2aa5a4748508e[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Jan 13 16:02:08 2015 -0800

    Update README.md

[33mcommit d5239cf464cb015503f56c8bd3575c2d4311f240[m
Merge: 690ebfc eb9a3e5
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Jan 13 15:57:58 2015 -0800

    Merge pull request #5 from sperez8/panel
    
    Panel

[33mcommit eb9a3e521699927311444ad060f0cd16f2e4ebc2[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Thu Dec 18 13:07:18 2014 -0500

    restructured layout of panel using percentages instead of absolute
    widths. Added axis labelling and legend

[33mcommit 2219e35fa07391c3f483560b269860e0bfbd54f6[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Fri Dec 12 18:23:05 2014 -0500

    implemented timer on mouseover events. ***needs debugging for low delay
    times***

[33mcommit badc35c7e9ee61424ffdac687152274d689d794e[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Thu Dec 11 17:41:24 2014 -0500

    commented methods. hovering over nodes and links only calls highlight
    methods for hovered over objects. Changed the functionality of 'click'.
    fixed an opacity issue: .attr() is not the same as .style() !!

[33mcommit 56f0290739cab890cf07b6380062a780e0ffafed[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Dec 10 18:50:52 2014 -0500

    Added an icon/button to remove rules.

[33mcommit a2a1f28e63263b1c16443ca0469889db7f03402a[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Dec 10 14:41:54 2014 -0500

    Filter button is now a checkbox.

[33mcommit f739cbd5fbbede0323f9889e07d10af89d1d6436[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Tue Dec 9 15:02:57 2014 -0500

    Node axis assignment can be evenly distributed so that the same number
    of nodes occur on each axis.

[33mcommit ba65928dd251a5764c25ba20e866bfea5109f3a5[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Dec 8 15:04:48 2014 -0500

    fixed log scaling of node positions for negative values.

[33mcommit fe772a6f37c253b112485c845b4cd13c35dcc644[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Wed Dec 3 14:52:04 2014 -0800

    log scaling works for node assignment as well

[33mcommit b50a254043f2970252c42cb8115b5552887c644e[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Wed Dec 3 08:34:29 2014 -0800

    fixed some log scale stuff and rounding values function for node information display

[33mcommit 1f6907463ecf517f513a90fc288716d6866a412f[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Dec 2 11:22:36 2014 -0800

    Fixed log scale for negative values

[33mcommit b889b95579b5f470acc32c611c8e30a763ed951e[m
Author: Sarah Perez <karatezeus21@gmail.com>
Date:   Tue Dec 2 10:55:28 2014 -0800

    implemented a modified log scale for domains with zero values

[33mcommit ff7d4113bbbea3bbbb35e98be327a986b9eb5c38[m
Author: Sarah Perez <sperez@shuttle.mi.microbiology.ubc.ca>
Date:   Thu Nov 27 08:49:24 2014 -0800

    fixed an opacity bug

[33mcommit 736fa967d38928f22dfe31535f8b2377ca5e4dd4[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 26 21:31:08 2014 -0800

    Added a class so that opacity of colored node consistently remains high
    than normal opacity through interactions

[33mcommit 26a8dc6a1f5ffa14e38da4ba76d2fd31922cd7cf[m
Author: Sarah Perez <sperez@shuttle.mi.microbiology.ubc.ca>
Date:   Tue Nov 25 12:40:30 2014 -0800

    measures per component and per node can be calculated.

[33mcommit d15b2273279d53fb645564110a480b3f9e8ce1e7[m
Author: Sarah Perez <sperez@shuttle.mi.microbiology.ubc.ca>
Date:   Tue Nov 25 11:43:14 2014 -0800

    import csv graph adds attributes to nodes and edges

[33mcommit a5846cf26e3966782a8d3fd31b96d9ed28848cf6[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 19 14:25:21 2014 -0800

    Fixed link drawing for number of axes > 3

[33mcommit 4638b66f7ea60c37c80ff86409437cf6e872b602[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 19 11:43:29 2014 -0800

    fixed tooltip so displays name of node and automatically adjusts width/height of tooltip boxes

[33mcommit 8b1d253fb5aa6e3203006898a6b0aeceb7bbbc5b[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 19 11:09:13 2014 -0800

    fixed the removal of the text showing how many marks were colored/filtered. Also, the nodes are now plotted on top of the links for better visuals

[33mcommit 639bd9714d2368f86bccf6e8e642621bd3a8579d[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 19 09:20:51 2014 -0800

    Fixed bugs on double axes. All possible links are being shown

[33mcommit c0b9423c7376b012765d93507f1627ae469ce124[m
Merge: 7aec0b7 5cda0d3
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 19 07:51:31 2014 -0800

    Merge branch 'panel' of https://github.com/sperez8/HivePlotter into panel

[33mcommit 5cda0d37dab3044ae5b2a34394b95d65e115328a[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Tue Nov 18 17:49:52 2014 -0800

    Hive panels can now include double axes.

[33mcommit 1e1eb2188bb93978b6bf4b24a0a1201388a76c97[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Tue Nov 18 13:31:10 2014 -0800

    cleaned up panel_methods.

[33mcommit 7aec0b73cd63f6f88fe95e7eede869762c2c9ac8[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 17 14:27:26 2014 -0800

    graph component is another network measure that can be plotted

[33mcommit 6cde1cd78426334bba938d7ff1fcf5f1ae395980[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 17 13:24:34 2014 -0800

    Fixed removal of links fron nodes on same axes that shouldn't be shown

[33mcommit e5b623d0ceae230f926a80f4a12626f6eafda702[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 17 12:57:39 2014 -0800

    for coloring and filtering queries, the number of modified items is showed.

[33mcommit 8521cb39375f3b4aa0ee5962303386ad5d86a568[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 17 11:50:52 2014 -0800

    Tooltip works for links as well. clicking on a link highlights the source and targets nodes on all hive plots

[33mcommit e1e40441891030ee8b5670f7dcd544fe2832a3db[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 17 11:24:30 2014 -0800

    Tooltip works and make nodes come to front when colored or searched for.

[33mcommit 33048faa3bd55698cac978bad934fd430f12e810[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 16 19:58:34 2014 -0800

    added tooltip for node positionning. nouse mouseover functions know work
    on click event.

[33mcommit 649ce3f73ef6e93166c45103fc7d08e2b35a02b4[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 16 18:59:22 2014 -0800

    removed link highlihgt on node mouse over event to prevent crashing.

[33mcommit 80080577d2362edeb11e94879872a79cdc9bc922[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 16 18:30:03 2014 -0800

    changed node and link reveal function to bold property names and
    increase the font size of the name of the node/link

[33mcommit eed54d05144197b2287076e63940e91132887980[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 16 18:09:50 2014 -0800

    fixed graphml reading/converter

[33mcommit a3d04f8ded9992f91c04d69bc41b756d8e9cced1[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Fri Nov 14 17:41:01 2014 -0800

    added method to convert graphml files to node and edge files.

[33mcommit b414c490d7c39283bde5b59c9f07134308ca810e[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Thu Nov 13 15:15:36 2014 -0800

    properties and values in form options are listed lexicographically. The categories for axis assignment and positioning are also sorted lexicographically. Attempting to fix opacity issues on queries, still in progress.

[33mcommit b53ce66c451ce5dad1e813b411f6a2a3ff0b3351[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Tue Nov 11 17:47:06 2014 -0800

    started writing a method to import graphml files

[33mcommit def067cce18d4d96aa88f591ddc9c39d4f0fb69b[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 10 15:52:38 2014 -0800

    Filtering nodes now propagates to their links, as it should.

[33mcommit d9477746b607481197895e8b861ad239ae3eb203[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 10 14:48:16 2014 -0800

    mend
    
    fixed filter. works lit it is supposed now. Reorganized webfiles into html layout, css, js methods and js parameter files

[33mcommit a320ce62bd69a5b47df2544541d8d05be9bed15a[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Mon Nov 10 14:47:21 2014 -0800

    fixed filter. works lit it is supposed now. Reorganized webfiles into html layout, css, js methods and js parameter files

[33mcommit fc934e3935440bbf56f0504c1d1e9d6ff61a1801[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 9 13:42:34 2014 -0800

    Changed styling of reveal area so that text doesn't overflow. All
    node/links attributes are displayed dynamically.

[33mcommit 501660ff44815e7ef0397390a57fff4f9b87f49d[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 9 12:22:27 2014 -0800

    Fixed positioning of nodes given categorical attributes. Using d3's
    rangeBands() scale

[33mcommit d894ffd2db595c65f181b1e7201d71b1a4d64011[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 9 11:49:25 2014 -0800

    fixed bug with node attributes which were numerical but stored as
    strings.

[33mcommit ee1f63106eb0ad3372e8f1657c60bbd9f98cb0ce[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 9 11:13:12 2014 -0800

    Axis assignment and positioning scales are printed to the console.

[33mcommit b736e07d309c45ad160e8c20f0865e1dd5304ddc[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Sun Nov 9 10:42:43 2014 -0800

    cleaned up tmp folder. Added d3 files so that panel html runs offline.

[33mcommit 8d91bf5319b15f8a7110e0b8f7faae455cbe0a3c[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Fri Nov 7 16:54:21 2014 -0800

    runpanel.py makes the node and edge file for panel_new_layout.html file. Also, categorical attributes are automatically scaled.

[33mcommit eea4877df3b29dce5bfa5c23a85dba0553ff7d84[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Thu Nov 6 11:44:08 2014 -0800

    made all viz text formatting standard and without using css for consistency on svg export

[33mcommit d4e5259798c37874e8bad6c735a31e3ab014d538[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Thu Nov 6 11:04:59 2014 -0800

    Made control panel css styling prettier and visually organized

[33mcommit 56eaa294ebe097b78f08ebba1da80f16acc3b1fb[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Thu Nov 6 09:24:06 2014 -0800

    Filtering in and out works. Changed css styling of rules

[33mcommit d1b14875648729c552d95a9b813b3335d38250a0[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 5 15:42:23 2014 -0800

    filtering and undoing filtering works when filtering 'out'. Filtering 'in' optin coming right up.

[33mcommit 0b7bb58bc9a055af3706be11dc0ced28ee457cc8[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 5 15:13:19 2014 -0800

    slowly adding filter functionality: can add and remove filter button and form

[33mcommit 7e71b75262bb8597fee71ea5162b041ae4099f8d[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 5 10:22:13 2014 -0800

    removed div enclosing 'Add rule' button for cleanliness

[33mcommit f1f9d1fb15500c6b42262e30023f706fffaa2abf[m
Author: sperez8 <karatezeus21@gmail.com>
Date:   Wed Nov 5 08:22:10 2014 -0800

    Fixed colorbox issue. Each work independently now.
